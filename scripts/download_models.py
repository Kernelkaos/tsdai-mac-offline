"""Download the model files once so the app can run fully offline.

Uses hf_hub_download directly with curl-compatible stream/chunk handling,
avoiding the experimental hf-xet / CAS protocol timeouts on unstable connections.

Usage:
    .venv/bin/python scripts/download_models.py
"""
import os
import sys
import time
from pathlib import Path

for var in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "DIFFUSERS_OFFLINE"):
    os.environ.pop(var, None)

# Force standard HTTP transfers instead of hf-xet CAS client
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

from huggingface_hub import hf_hub_download  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

FILES_TO_DOWNLOAD = [
    # SDXL Base 1.0 (Essential weights)
    ("stabilityai/stable-diffusion-xl-base-1.0", "model_index.json", "models/sdxl-base-1.0/model_index.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "scheduler/scheduler_config.json", "models/sdxl-base-1.0/scheduler/scheduler_config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer/tokenizer_config.json", "models/sdxl-base-1.0/tokenizer/tokenizer_config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer/vocab.json", "models/sdxl-base-1.0/tokenizer/vocab.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer/merges.txt", "models/sdxl-base-1.0/tokenizer/merges.txt"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer/special_tokens_map.json", "models/sdxl-base-1.0/tokenizer/special_tokens_map.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer_2/tokenizer_config.json", "models/sdxl-base-1.0/tokenizer_2/tokenizer_config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer_2/vocab.json", "models/sdxl-base-1.0/tokenizer_2/vocab.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer_2/merges.txt", "models/sdxl-base-1.0/tokenizer_2/merges.txt"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "tokenizer_2/special_tokens_map.json", "models/sdxl-base-1.0/tokenizer_2/special_tokens_map.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "text_encoder/config.json", "models/sdxl-base-1.0/text_encoder/config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "text_encoder/model.fp16.safetensors", "models/sdxl-base-1.0/text_encoder/model.fp16.safetensors"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "text_encoder_2/config.json", "models/sdxl-base-1.0/text_encoder_2/config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "text_encoder_2/model.fp16.safetensors", "models/sdxl-base-1.0/text_encoder_2/model.fp16.safetensors"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "unet/config.json", "models/sdxl-base-1.0/unet/config.json"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "unet/diffusion_pytorch_model.fp16.safetensors", "models/sdxl-base-1.0/unet/diffusion_pytorch_model.fp16.safetensors"),

    # ControlNet Canny SDXL 1.0 (~2.5 GB)
    ("diffusers/controlnet-canny-sdxl-1.0", "config.json", "models/controlnet-canny-sdxl-1.0/config.json"),
    ("diffusers/controlnet-canny-sdxl-1.0", "diffusion_pytorch_model.fp16.safetensors", "models/controlnet-canny-sdxl-1.0/diffusion_pytorch_model.fp16.safetensors"),

    # VAE fp16 fix (~330 MB)
    ("madebyollin/sdxl-vae-fp16-fix", "config.json", "models/sdxl-vae-fp16-fix/config.json"),
    ("madebyollin/sdxl-vae-fp16-fix", "diffusion_pytorch_model.safetensors", "models/sdxl-vae-fp16-fix/diffusion_pytorch_model.safetensors"),
]


def download_with_retry(repo_id: str, filename: str, target_rel_path: str, max_retries: int = 5) -> bool:
    target_path = ROOT / target_rel_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists() and target_path.stat().st_size > 0:
        print(f"✓ Already present: {target_rel_path}")
        return True

    print(f"\n--> Downloading: {repo_id} : {filename}")
    for attempt in range(1, max_retries + 1):
        try:
            downloaded = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                local_dir=target_path.parent,
            )
            # Ensure proper filename match if downloaded directly
            dest_name = Path(filename).name
            actual_file = target_path.parent / dest_name
            if actual_file.exists() and actual_file != target_path:
                actual_file.rename(target_path)

            print(f"✓ Completed: {target_rel_path}")
            return True
        except Exception as err:
            print(f"! Attempt {attempt}/{max_retries} failed for {filename}: {err}")
            time.sleep(3)

    return False


def main() -> int:
    failed = []
    for repo_id, filename, rel_path in FILES_TO_DOWNLOAD:
        success = download_with_retry(repo_id, filename, rel_path)
        if not success:
            failed.append(rel_path)

    if failed:
        print("\nSome files could not be downloaded completely:")
        for f in failed:
            print(f"  - {f}")
        print("\nPlease check your internet connection and re-run to resume.")
        return 1

    print("\n✓ ALL MODELS DOWNLOADED SUCCESSFULLY!")
    print("You can now run Tsdai completely offline via ./scripts/run.sh or the Desktop shortcut.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
