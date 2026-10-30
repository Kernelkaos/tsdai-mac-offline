from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import psutil
import torch
import yaml
from diffusers import AutoencoderKL, ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageOps

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
}


class ModelsNotFoundError(RuntimeError):
    """Raised when local model files are missing."""


class InsufficientMemoryError(RuntimeError):
    """Raised when available memory is below safety threshold."""


class ImageTransformerEngine:
    """SDXL + ControlNet Canny pipeline reading exclusively from local files (Apple Silicon)."""

    def __init__(self, config_path: str | Path | None = None):
        self.config = self._load_config(Path(config_path) if config_path else ROOT / "config" / "settings.yaml")
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.pipe = None

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
        low_threshold: int = 100,
        high_threshold: int = 200,
        seed: int = -1,
        target_size: tuple[int, int] = (896, 1152),
    ) -> Image.Image:
        """Execute SDXL + ControlNet Canny inference loop."""
        self.load_models()

        inf = self.config["inference"]
        steps = inf["default_steps"] if steps is None else steps
        guidance_scale = inf["default_guidance_scale"] if guidance_scale is None else guidance_scale
        controlnet_scale = inf["controlnet_conditioning_scale"] if controlnet_scale is None else controlnet_scale

        # Ajusta a imagem de forma proporcional sem esticar
        fitted_input = self.fit_image_proportionally(input_image, target_size)

        canny = self.process_canny_image(fitted_input, low_threshold, high_threshold, target_size=target_size)
        generator = torch.Generator(device="cpu").manual_seed(seed) if seed != -1 else None

        self.check_free_memory()
        try:
            with VRAMGuard():
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=canny,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    controlnet_conditioning_scale=controlnet_scale,
                    generator=generator,
                    width=target_size[0],
                    height=target_size[1],
                )
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                raise InsufficientMemoryError(
                    "The GPU memory limit was reached. Close other apps or lower resolution in config/settings.yaml."
                ) from e
            raise
        return result.images[0]
