# Presets de estilos, iluminação, liberdade criativa e enriquecedor de prompts

from src.core.translator import translate_pt_to_en

STYLE_PRESETS = {
    "Retrato Fotográfico de Estúdio": {
        "folder": "studio_portrait",
        "prompt_prefix": "professional photo of ",
        "prompt_suffix": (
            ", 85mm portrait lens, f/2.0 aperture, balanced studio lighting, "
            "sharp focus, natural realistic skin texture, highly detailed, raw photo, realistic shadows"
        ),
        "negative_suffix": (
            ", (airbrushed:1.4), (plastic skin:1.4), (oversaturated:1.3), shiny skin, "
            "cartoon, 3d render, illustration, deformed limbs, malformed body, mutant, caricature"
        ),
        "default_cfg": 5.0,
    },
    "Cena Cinematográfica de Filme": {
        "folder": "cinematic",
        "prompt_prefix": "cinematic movie scene of ",
        "prompt_suffix": (
            ", 35mm anamorphic lens, realistic cinematic lighting, film color grading, "
            "subtle volumetric light, high production value, photorealistic, 35mm film grain"
        ),
        "negative_suffix": (
            ", cartoon, anime, 3d render, plastic, oversaturated, overexposed, amateur, deformed, caricature"
        ),
        "default_cfg": 5.0,
    },
    "Arte Conceitual & Pintura Digital": {
        "folder": "concept_art",
        "prompt_prefix": "concept art illustration of ",
        "prompt_suffix": (
            ", trending on ArtStation, dynamic lighting, masterwork, intricate brushwork, "
            "atmospheric perspective, rich color palette, epic scale"
        ),
        "negative_suffix": ", photo, realistic photo, ugly, deformed, text, watermark, signature",
        "default_cfg": 6.5,
    },
    "Anime & Mangá Moderno": {
        "folder": "anime_manga",
        "prompt_prefix": "modern anime aesthetic illustration of ",
        "prompt_suffix": (
            ", Makoto Shinkai style, vibrant colors, clean crisp line art, "
            "beautiful lighting and clouds, high detail anime masterpiece"
        ),
        "negative_suffix": ", photograph, 3d render, realistic skin, deformed, poorly drawn hands, blurry",
        "default_cfg": 6.5,
    },
    "Cyberpunk & Ficção Científica": {
        "folder": "cyberpunk_scifi",
        "prompt_prefix": "cyberpunk sci-fi scene of ",
        "prompt_suffix": (
            ", neon accents, realistic lighting reflections, wet pavement, "
            "futuristic atmosphere, cinematic film still, photorealistic"
        ),
        "negative_suffix": ", vintage, daytime, pastoral, washed out, cartoon, oversaturated cartoon, deformed",
        "default_cfg": 5.5,
    },
    "Livre (Sem estilo predefinido)": {
        "folder": "freeform",
        "prompt_prefix": "",
        "prompt_suffix": "",
        "negative_suffix": ", deformed, cartoon, oversaturated, plastic, distorted",
        "default_cfg": 5.0,
    },
}

LIGHTING_MOODS = {
    "Natural Suave de Estúdio (Softbox)": "soft diffused studio lighting, gentle ambient light, flattering exposure",
    "Golden Hour (Luz Dourada de Entardecer)": "natural warm golden hour light, soft rim lighting, warm glow",
    "Luz Natural de Janela": "soft natural window lighting, gentle realistic falloff, natural indoor ambiance",
    "Cinematográfica Moody": "subtle moody cinematic lighting, natural shadows, controlled contrast",
    "Neon Sutil / Cyberpunk": "subtle neon ambient highlights, cyan and warm tones, realistic street reflection",
    "Nenhum (Iluminação Natural da Foto)": "",
}

CREATIVE_FREEDOM_LEVELS = {
    "Equilibrado (Recomendado: Rosto/Postura idênticos + Realismo)": {"control_scale": 0.65, "cfg": 5.0},
    "Fiel / Anatômico (Mantém o corpo, pose e roupas quase intactos)": {"control_scale": 0.85, "cfg": 4.5},
    "Criativo / Estilizado (Permite inventar roupas e fundos novos)": {"control_scale": 0.50, "cfg": 5.5},
}

ASPECT_RATIOS = {
    "Retrato / Vertical (896 x 1152) [Ideal para Pessoas]": (896, 1152),
    "Quadrado (1024 x 1024) [Padrão Redes Sociais]": (1024, 1024),
    "Paisagem / Horizontal (1152 x 896) [Cinema e Ambientes]": (1152, 896),
}


def enhance_prompt_magic(prompt: str) -> str:
    """Enriquece prompts sem forçar termos conflitantes como rostos em fotos de costas."""
    cleaned = prompt.strip()
    if not cleaned:
        return "natural realistic photography, sharp focus, professional quality"

    # Não força 'facial features' se o usuário estiver pedindo foto de costas/corpo
    if any(k in cleaned.lower() for k in ["costas", "behind", "back"]):
        return f"{cleaned}, anatomically correct body, natural skin texture, realistic posture, master photography"

    words = cleaned.split()
    if len(words) < 8:
        return f"{cleaned}, natural realistic photography, sharp focus, authentic texture, master quality"
    return cleaned


def apply_style_and_lighting(
    style_name: str,
    lighting_name: str,
    prompt: str,
    negative_prompt: str,
    magic_enabled: bool = True,
):
    preset = STYLE_PRESETS.get(style_name, STYLE_PRESETS["Livre (Sem estilo predefinido)"])

    # Traduz termos em português para inglês fotográfico
    translated_prompt = translate_pt_to_en(prompt)

    base_prompt = enhance_prompt_magic(translated_prompt) if magic_enabled else translated_prompt.strip()
    lighting_tag = LIGHTING_MOODS.get(lighting_name, "")

    parts = [preset["prompt_prefix"], base_prompt]
    if lighting_tag:
        parts.append(f", {lighting_tag}")
    parts.append(preset["prompt_suffix"])

    final_prompt = "".join(parts).strip()

    if negative_prompt and negative_prompt.strip():
        translated_neg = translate_pt_to_en(negative_prompt)
        final_neg = f"{translated_neg.strip()}{preset['negative_suffix']}"
    else:
        final_neg = preset["negative_suffix"].lstrip(", ")

    return final_prompt, final_neg, preset["folder"]
