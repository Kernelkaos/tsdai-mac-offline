import time
from pathlib import Path
import torch
from PIL import Image, ImageOps
import cv2
import numpy as np
from diffusers import AutoencoderKL, ControlNetModel, StableDiffusionXLControlNetPipeline
from transformers import CLIPVisionModelWithProjection, CLIPImageProcessor

ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = Path("/Users/mac/.gemini/antigravity/brain/0a632adc-4f1f-4cc3-a8e3-cfe8ac222e20/.user_uploaded/media_1793367959187_a6741691.jpg")
OUTPUT_DIR = Path("/Users/mac/Pictures/Tsdai_Outputs/studio_portrait")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "teste_modelo_biquini.png"

device = "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float16 if device == "mps" else torch.float32

print(f"=== INICIANDO TESTE BENCHMARK COM IP-ADAPTER + CONTROLNET ===")
print(f"Dispositivo: {device} (Apple Silicon Metal Performance Shaders)")
print(f"Imagem de entrada: {IMAGE_PATH}")

t_start = time.time()

# 1. Carregar componentes locais
print("\n[1/4] Carregando modelos locais...")
vae = AutoencoderKL.from_pretrained(
    ROOT / "models/sdxl-vae-fp16-fix",
    torch_dtype=dtype,
    local_files_only=True
)

controlnet = ControlNetModel.from_pretrained(
    ROOT / "models/controlnet-canny-sdxl-1.0",
    variant="fp16",
    torch_dtype=dtype,
    local_files_only=True
)

pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    ROOT / "models/sdxl-base-1.0",
    controlnet=controlnet,
    vae=vae,
    variant="fp16",
    torch_dtype=dtype,
    local_files_only=True
).to(device)

image_encoder = CLIPVisionModelWithProjection.from_pretrained(
    ROOT / "models/image_encoder",
    torch_dtype=dtype,
    local_files_only=True
).to(device)

feature_extractor = CLIPImageProcessor()
pipe.register_modules(image_encoder=image_encoder, feature_extractor=feature_extractor)

pipe.load_ip_adapter(
    str(ROOT / "models/ip_adapter"),
    subfolder="",
    weight_name="ip-adapter-plus-face_sdxl_vit-h.safetensors",
    image_encoder_folder=None,
    local_files_only=True
)

print(f"Tempo de carregamento dos pesos: {time.time() - t_start:.2f}s")

# 2. Preparar imagem de entrada
print("\n[2/4] Processando geometria da imagem...")
input_img = Image.open(IMAGE_PATH).convert("RGB")
# Proporção SDXL 768x1344 (formato vertical/retrato 9:16)
target_size = (768, 1344)
fitted_img = ImageOps.fit(input_img, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

# Canny edges
img_bgr = cv2.cvtColor(np.array(fitted_img), cv2.COLOR_RGB2BGR)
edges = cv2.Canny(img_bgr, 120, 220)
canny_img = Image.fromarray(np.stack([edges] * 3, axis=2))

# Face crop ou imagem de referência para o IP-Adapter
# O IP-Adapter Face recebe a foto da modelo para extrair a fisionomia exata
ip_adapter_ref = fitted_img

# 3. Configurar balanço Identidade vs Posição
# IP-Adapter Scale: 0.75 (alta fidelidade da pessoa)
# ControlNet Scale: 0.38 (mantém pose, ângulo e curvas corporais sem prender a roupa anterior)
ip_scale = 0.75
pipe.set_ip_adapter_scale(ip_scale)
cnet_scale = 0.38

prompt = (
    "award-winning photographic portrait of the same beautiful Brazilian woman, "
    "semi-profile from behind, looking over shoulder at camera smiling warmly, "
    "wearing a stylish elegant bikini swimwear, bare back, fit athletic body, "
    "curly long dark hair, natural freckles on cheeks, glowing sun-kissed skin, "
    "standing on a tropical sandy beach with ocean waves and palm trees in soft blurred background, "
    "sunset golden hour warm directional lighting, 8k uhd, dslr photo, high resolution, hyperrealistic"
)

negative_prompt = (
    "t-shirt, shorts, cotton clothing, crop top, oversized clothes, "
    "bad anatomy, deformed face, bad eyes, disfigured hands, extra limbs, "
    "ugly, blurry, low quality, oversaturated, plastic skin, cartoon, anime, 3d render, painting"
)

steps = 40
guidance_scale = 5.0
seed = 42
generator = torch.Generator(device="cpu").manual_seed(seed)

print(f"\n[3/4] Gerando imagem ({steps} passos, guidance={guidance_scale}, seed={seed})...")
print(f"Fidelidade da Identidade (IP-Adapter): {ip_scale}")
print(f"Fidelidade da Postura (ControlNet): {cnet_scale}")

t_gen_start = time.time()
result = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=canny_img,
    ip_adapter_image=ip_adapter_ref,
    num_inference_steps=steps,
    guidance_scale=guidance_scale,
    controlnet_conditioning_scale=cnet_scale,
    generator=generator,
    width=target_size[0],
    height=target_size[1],
)
gen_duration = time.time() - t_gen_start
print(f"Tempo de inferência: {gen_duration:.2f} segundos!")

# 4. Salvar resultado
out_image = result.images[0]
out_image.save(OUTPUT_PATH)
print(f"\n[4/4] Imagem salva com sucesso em:\n{OUTPUT_PATH}")
print(f"Tempo total de execução: {time.time() - t_start:.2f}s")
