"""AI Image Transformer (Mac, offline) - command-line launcher.

Offline mode and the GPU memory cap are applied before any library is imported, so no
network request can be made at runtime and the app cannot exhaust the Mac's memory.
Models must already be in ./models (see scripts/download_models.py).
"""
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent

# Must be set before importing huggingface / transformers / diffusers / gradio.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["DIFFUSERS_OFFLINE"] = "1"
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"


def _apply_memory_cap() -> None:
    """Set the PyTorch MPS memory cap from config/settings.yaml (must run before importing torch)."""
    with open(ROOT / "config" / "settings.yaml", encoding="utf-8") as f:
        ratio = float((yaml.safe_load(f).get("memory") or {}).get("gpu_memory_limit_ratio", 1.0))
    if not 0.1 <= ratio <= 1.0:
        raise SystemExit(
            f"Invalid memory.gpu_memory_limit_ratio = {ratio}. Use a value from 0.1 to 1.0. "
            "A value of 0 would remove the limit and can freeze the Mac, so it is not allowed."
        )
    # The low watermark must not be higher than the high watermark.
    os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = str(ratio)
    os.environ["PYTORCH_MPS_LOW_WATERMARK_RATIO"] = str(round(ratio * 0.9, 3))


_apply_memory_cap()

import argparse  # noqa: E402
import sys  # noqa: E402

from src.core.engine import ImageTransformerEngine, ModelsNotFoundError  # noqa: E402
from src.ui.dashboard import create_dashboard  # noqa: E402

HOST = "127.0.0.1"  # fixed on purpose: the app is never exposed to the network


def main():
    parser = argparse.ArgumentParser(description="AI Image Transformer (Mac, offline)")
    parser.add_argument("--port", type=int, default=7860, help="Local port (default: 7860)")
    args = parser.parse_args()

    try:
        engine = ImageTransformerEngine()
        engine.check_models()
    except ModelsNotFoundError as e:
        print(f"\n{e}\n", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, KeyError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Device: {engine.device}")
    if engine.config["performance"].get("preload_model"):
        print("Loading the model into memory (this takes a minute)...")
        engine.load_models()
        print("Model ready.")

    dashboard = create_dashboard(engine)
    print(f"Open http://{HOST}:{args.port} (offline mode, local access only)")
    dashboard.launch(
        server_name=HOST,
        server_port=args.port,
        share=False,
        theme=dashboard.launch_theme,
    )


if __name__ == "__main__":
    main()
