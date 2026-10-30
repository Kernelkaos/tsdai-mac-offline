"""Download the IP-Adapter SDXL face models for zero-shot identity preservation."""
import os
import sys
import time
from pathlib import Path

for var in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "DIFFUSERS_OFFLINE"):
    os.environ.pop(var, None)

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

from huggingface_hub import hf_hub_download  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

IP_FILES = [
    # Image Encoder ViT-H
    ("h94/IP-Adapter", "models/image_encoder/config.json", "models/image_encoder/config.json"),
    ("h94/IP-Adapter", "models/image_encoder/model.safetensors", "models/image_encoder/model.safetensors"),
    # IP-Adapter Face SDXL
    ("h94/IP-Adapter", "sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors", "models/ip_adapter/ip-adapter-plus-face_sdxl_vit-h.safetensors"),
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
            downloaded = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=target_path.parent)
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
    print("=== Downloading IP-Adapter SDXL FaceID Weights (~3.3 GB) ===")
    failed = []
    for repo_id, filename, rel_path in IP_FILES:
        if not download_with_retry(repo_id, filename, rel_path):
            failed.append(rel_path)

    if failed:
        print("\nSome IP-Adapter files failed to download. Check connection and re-run.")
        return 1

    print("\n✓ ALL IP-ADAPTER MODELS READY!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
