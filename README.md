# Tsdai — AI Image Transformer (Mac Apple Silicon Offline)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue.svg)
![Apple Silicon](https://img.shields.io/badge/hardware-Apple%20Silicon%20(MPS)-silver.svg)
![Mode](https://img.shields.io/badge/runtime-100%25%20Offline-success.svg)

High-fidelity image-to-image transformation pipeline powered by **Stable Diffusion XL (SDXL)** and **ControlNet Canny**. Engineered specifically for macOS on Apple Silicon (M1/M2/M3/M4) leveraging unified memory architecture for zero-latency, private, and fully offline generation.

---

## 🌟 Key Features & Custom Engineering

- **100% Offline Air-Gapped Execution:** Network calls are strictly disabled at the environment and library layer (`HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, `DIFFUSERS_OFFLINE`). No external telemetry, no Google Fonts, and no public tunneling.
- **Unified Memory Optimization:** Tuned for high-memory Apple Silicon configurations (64 GB). Attention slicing and VAE tiling are turned off by default, yielding a **~15%–35% speedup** with zero degradation in pixel sharpness.
- **Hardware Memory Safety Guard:** Includes a high-watermark cap (`PYTORCH_MPS_HIGH_WATERMARK_RATIO = 1.0`, ~80% of RAM) alongside a pre-generation RAM availability check. System freezes or forced kernel swaps are prevented.
- **43-Step Quality Sweet Spot:** Default steps calibrated to **43 steps**, delivering peak studio-grade texture resolution (skin pores, hair, fabrics) without the over-baking artifacts common at 50+ steps.
- **Dual-Gauge Precision Controls:**
  - *Inference Steps Gauge (43):* Visual feedback on speed vs. texture fidelity.
  - *ControlNet Influence Gauge (0.50):* Calibrates edge rigidity against generative lighting and shadow synthesis.
- **Aspect Ratio Distortion Prevention:** Support for native 1-Megapixel resolutions (Square `1024x1024`, Portrait `896x1152`, and Landscape `1152x896`).
- **Instant Canny Edge Detection Preview:** Sub-100ms CPU-based OpenCV preview of structural contours prior to running diffusion.
- **Automatic Style-Based Output Cataloging:** Generated outputs are saved with lossless PNG compression directly into `~/Pictures/Tsdai_Outputs/<style_category>/` paired with a corresponding JSON metadata sidecar documenting the full reproduction parameters.
- **Universal Portability:** Includes `install.sh` for one-command deployment across any Apple Silicon Mac.

---

## 📂 Output Catalog Structure

Images and reproduction metadata are organized into discrete folders inside your user's Pictures directory:

```text
~/Pictures/Tsdai_Outputs/
├── studio_portrait/
│   ├── img_20261029_130520_s42.png
│   └── img_20261029_130520_s42.json
├── cinematic/
├── concept_art/
├── anime_manga/
├── cyberpunk_scifi/
└── freeform/
```

---

## ⚙️ Quality & Performance Configuration Reference

Settings are stored in [`config/settings.yaml`](config/settings.yaml):

| Parameter | Default | Purpose & Architectural Notes |
|---|---|---|
| `inference.default_steps` | `43` | High-fidelity sweet spot. Balanced texture depth without contrast burn. |
| `inference.controlnet_conditioning_scale` | `0.5` | Edge adherence ratio. Values between 0.40–0.55 allow natural lighting synthesis. |
| `performance.enable_attention_slicing` | `false` | Memory-saving computation splitting. Disabled on 64 GB Macs for maximum throughput. |
| `performance.enable_vae_tiling` | `false` | Disabled to eliminate tile boundary seams in rendered outputs. |
| `performance.preload_model` | `true` | Preloads weights into unified memory at launcher boot to eliminate first-render lag. |
| `memory.gpu_memory_limit_ratio` | `1.0` | Restricts PyTorch MPS allocations to OS-recommended GPU maximum (~51.8 GB on 64 GB Mac). |
| `memory.min_free_memory_gb` | `12` | Pre-flight check refusing execution if free RAM drops below safe operating limits. |

### Recommended Hardware Allocations

| Unified Memory | `enable_attention_slicing` | `enable_vae_tiling` | `gpu_memory_limit_ratio` | `min_free_memory_gb` |
|---|---|---|---|---|
| **64 GB or more** | `false` | `false` | `1.0` | `12` |
| **32 GB** | `false` | `true` | `0.9` | `8` |
| **16 GB** | `true` | `true` | `0.8` | `4` |

---

## 🚀 Installation & First-Time Setup

### 1. Clone & Automated Install
```bash
git clone https://github.com/Kernelkaos/ai-image-transformer-mac-offline.git
cd ai-image-transformer-mac-offline

./install.sh
```

### 2. Download Local Weights (One-Time Setup)
Model weights (~9.5 GB in total, fp16 safetensors) must be downloaded once:
```bash
.venv/bin/python scripts/download_models.py
```
*Note: This download script is resumable. If your network connection drops, simply re-run it.*

### 3. Launching
You may now disconnect completely from the internet:
```bash
./scripts/run.sh
```
Or double-click the **Tsdai** desktop shortcut created on your macOS Desktop. Open your browser to <http://127.0.0.1:7860>.

---

## 📄 License

Distributed under the [MIT License](LICENSE). Underlying foundation models (SDXL 1.0, ControlNet) are governed by their respective OpenRAIL licenses.
