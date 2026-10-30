from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import psutil
import torch
import yaml
from diffusers import AutoencoderKL, ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageOps
from transformers import CLIPImageProcessor, CLIPVisionModelWithProjection

from src.core.memory import VRAMGuard

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = {
    "sdxl_base": [
        "model_index.json",
        "unet/diffusion_pytorch_model.fp16.safetensors",
        "text_encoder/model.fp16.safetensors",
        "text_encoder_2/model.fp16.safetensors",
    ],
    "controlnet_canny": ["config.json", "diffusion_pytorch_model.fp16.safetensors"],
    "vae": ["config.json", "diffusion_pytorch_model.safetensors"],
    "image_encoder": ["config.json", "model.safetensors"],
    "ip_adapter": ["ip-adapter-plus-face_sdxl_vit-h.safetensors"],
}


class ModelsNotFoundError(RuntimeError):
    """Raised when local model files are missing."""


class InsufficientMemoryError(RuntimeError):
    """Raised when available memory is below safety threshold."""


class ImageTransformerEngine:
    """SDXL + ControlNet Canny + IP-Adapter Face pipeline reading exclusively from local files (Apple Silicon)."""

    def __init__(self, config_path: str | Path | None = None):
        self.config = self._load_config(Path(config_path) if config_path else ROOT / "config" / "settings.yaml")
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.pipe = None
        self.has_ip_adapter = False

    def _load_config(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _model_path(self, key: str) -> Path:
        return ROOT / self.config["paths"][key]

    def check_models(self) -> None:
        """Raise ModelsNotFoundError listing any missing model weights."""
        missing = []
        for key, files in REQUIRED_FILES.items():
            base = self._model_path(key)
            missing += [str(base / f) for f in files if not (base / f).exists()]
        if missing:
            listing = "\n  - ".join(missing)
            raise ModelsNotFoundError(
                "Model files are missing:\n  - "
                + listing
                + "\n\nDownload them once (internet required) with:\n  .venv/bin/python scripts/download_models.py"
            )

    def load_models(self) -> None:
        """Load pipeline from local weights with zero network calls."""
        if self.pipe is not None:
            return
        self.check_models()

        perf = self.config["performance"]
        dtype = torch.float16 if self.device == "mps" else torch.float32
        variant = "fp16" if dtype == torch.float16 else None
        common = {"torch_dtype": dtype, "local_files_only": True, "use_safetensors": True}

        vae = AutoencoderKL.from_pretrained(self._model_path("vae"), **common)
        controlnet = ControlNetModel.from_pretrained(self._model_path("controlnet_canny"), variant="fp16", **common)
        self.pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
            self._model_path("sdxl_base"), controlnet=controlnet, vae=vae, variant="fp16", **common
        )
        if variant is None:
            self.pipe.to(torch.float32)
        self.pipe.to(self.device)

        # Carregar IP-Adapter Face SDXL (LoRA Instantânea de Identidade)
        image_encoder_path = self._model_path("image_encoder")
        ip_adapter_path = self._model_path("ip_adapter")
        ip_weight = ip_adapter_path / "ip-adapter-plus-face_sdxl_vit-h.safetensors"

        if (image_encoder_path / "model.safetensors").exists() and ip_weight.exists():
            image_encoder = CLIPVisionModelWithProjection.from_pretrained(
                image_encoder_path, torch_dtype=dtype, local_files_only=True
            ).to(self.device)
            feature_extractor = CLIPImageProcessor()
            self.pipe.register_modules(image_encoder=image_encoder, feature_extractor=feature_extractor)

            self.pipe.load_ip_adapter(
                str(ip_adapter_path),
                subfolder="",
                weight_name="ip-adapter-plus-face_sdxl_vit-h.safetensors",
                image_encoder_folder=None,
                local_files_only=True,
            )
            self.has_ip_adapter = True

        if perf.get("enable_attention_slicing"):
            self.pipe.enable_attention_slicing()
        if perf.get("enable_vae_tiling"):
            self.pipe.enable_vae_tiling()

    def check_free_memory(self) -> None:
        """Verify unified memory before kicking off generation."""
        minimum = float(self.config.get("memory", {}).get("min_free_memory_gb", 0))
        available = psutil.virtual_memory().available / (1024**3)
        if available < minimum:
            raise InsufficientMemoryError(
                f"Only {available:.1f} GB of memory is currently available (minimum {minimum:g} GB required). "
                "Please close heavy background applications and retry."
            )

    @staticmethod
    def fit_image_proportionally(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
        """Encaixa a imagem na resolução alvo preservando as proporções naturais sem esticar."""
        return ImageOps.fit(image, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    @staticmethod
    def process_canny_image(
        image: Image.Image,
        low_threshold: int = 100,
        high_threshold: int = 200,
        target_size: tuple[int, int] | None = None,
    ) -> Image.Image:
        """Extract Canny edge lines formatted for ControlNet input."""
        if target_size and image.size != target_size:
            image = ImageTransformerEngine.fit_image_proportionally(image, target_size)
        img_bgr = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        edges = cv2.Canny(img_bgr, low_threshold, high_threshold)
        return Image.fromarray(np.stack([edges] * 3, axis=2))

    def generate(
        self,
        input_image: Image.Image,
        prompt: str,
        negative_prompt: str = "",
        steps: int | None = None,
        guidance_scale: float | None = None,
        controlnet_scale: float | None = None,
        ip_adapter_scale: float | None = None,
        control_guidance_end: float | None = None,
        reference_image: Image.Image | None = None,
        low_threshold: int = 100,
        high_threshold: int = 200,
        seed: int = -1,
        target_size: tuple[int, int] = (768, 1344),
    ) -> Image.Image:
        """Execute SDXL + ControlNet Canny + IP-Adapter inference loop."""
        self.load_models()

        inf = self.config["inference"]
        steps = inf.get("default_steps", 35) if steps is None else steps
        guidance_scale = inf.get("default_guidance_scale", 5.0) if guidance_scale is None else guidance_scale
        cnet_default = inf.get("controlnet_conditioning_scale", 0.35)
        controlnet_scale = cnet_default if controlnet_scale is None else controlnet_scale
        ip_adapter_scale = inf.get("ip_adapter_scale", 0.80) if ip_adapter_scale is None else ip_adapter_scale
        guidance_end_def = inf.get("control_guidance_end", 0.35)
        control_guidance_end = guidance_end_def if control_guidance_end is None else control_guidance_end

        # Encaixa a imagem de entrada de forma proporcional sem distorção
        fitted_input = self.fit_image_proportionally(input_image, target_size)
        canny = self.process_canny_image(fitted_input, low_threshold, high_threshold, target_size=target_size)

        generator = torch.Generator(device="cpu").manual_seed(seed) if seed != -1 else None

        pipe_kwargs = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image": canny,
            "num_inference_steps": steps,
            "guidance_scale": guidance_scale,
            "controlnet_conditioning_scale": controlnet_scale,
            "control_guidance_start": 0.0,
            "control_guidance_end": control_guidance_end,
            "generator": generator,
            "width": target_size[0],
            "height": target_size[1],
        }

        if self.has_ip_adapter:
            ref = reference_image if reference_image is not None else fitted_input
            self.pipe.set_ip_adapter_scale(ip_adapter_scale)
            pipe_kwargs["ip_adapter_image"] = ref

        self.check_free_memory()
        try:
            with VRAMGuard():
                result = self.pipe(**pipe_kwargs)
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                raise InsufficientMemoryError(
                    "The GPU memory limit was reached. Close other apps or lower resolution in config/settings.yaml."
                ) from e
            raise
        return result.images[0]
