# Presets de estilos, iluminação, liberdade criativa e enriquecedor de prompts

STYLE_PRESETS = {
    "Retrato Fotográfico de Estúdio": {
        "folder": "studio_portrait",
        "prompt_prefix": "professional studio portrait photograph of ",
        "prompt_suffix": (
            ", 85mm portrait lens, f/1.8 aperture, studio key lighting, "
            "sharp focus, natural skin texture, highly detailed, 8k resolution, raw photo"
        ),
        "negative_suffix": (
            ", (blurry:1.2), (airbrushed:1.2), (plastic skin:1.3), oversaturated, "
            "cartoon, drawing, illustration, deformed, distorted, duplicate"
        ),
        "default_cfg": 7.0,
    },
    "Cena Cinematográfica de Filme": {
        "folder": "cinematic",
        "prompt_prefix": "cinematic movie screengrab of ",
        "prompt_suffix": (
            ", 35mm anamorphic lens, dramatic moody lighting, color graded, volumetric fog, "
            "high production value, cinematic composition, photorealistic, 8k"
        ),
        "negative_suffix": ", cartoon, anime, 3d render, plastic, overexposed, amateur, low quality",
        "default_cfg": 7.5,
    },
    "Arte Conceitual & Pintura Digital": {
        "folder": "concept_art",
        "prompt_prefix": "concept art illustration of ",
        "prompt_suffix": (
            ", trending on ArtStation, dynamic lighting, masterwork, intricate brushwork, "
            "atmospheric perspective, rich color palette, epic scale"
        ),
        "negative_suffix": ", photo, realistic photo, ugly, deformed, text, watermark, signature",
        "default_cfg": 8.0,
    },
    "Anime & Mangá Moderno": {
        "folder": "anime_manga",
        "prompt_prefix": "modern anime aesthetic illustration of ",
        "prompt_suffix": (
            ", Makoto Shinkai style, vibrant colors, clean crisp line art, "
            "beautiful lighting and clouds, high detail anime masterpiece"
        ),
        "negative_suffix": ", photograph, 3d render, realistic skin, deformed, poorly drawn hands, blurry",
        "default_cfg": 7.5,
    },
    "Cyberpunk & Ficção Científica": {
        "folder": "cyberpunk_scifi",
        "prompt_prefix": "cyberpunk sci-fi scene of ",
        "prompt_suffix": (
            ", neon soaked streets, glowing holographic reflections, rainy wet pavement, "
            "high tech futuristic atmosphere, cinematic lighting, 8k"
        ),
        "negative_suffix": ", vintage, daytime, pastoral, washed out, low resolution",
        "default_cfg": 7.5,
    },
    "Livre (Sem estilo predefinido)": {
        "folder": "freeform",
        "prompt_prefix": "",
        "prompt_suffix": "",
        "negative_suffix": "",
        "default_cfg": 7.5,
    },
}

LIGHTING_MOODS = {
    "Natural de Estúdio (Softbox)": "soft diffused studio softbox lighting, even fill light, flattering illumination",
    "Golden Hour (Luz Dourada do Entardecer)": "warm sunset golden hour sunlight, soft rim lighting, golden glow",
    "Cinematográfica Dramática (Moody Chiaroscuro)": (
        "dramatic chiaroscuro lighting, deep cinematic shadows, high contrast edge light"
    ),
    "Neon Cyberpunk (Luzes Coloridas)": "vibrant dual-tone neon lighting, cyan and magenta highlights, reflections",
    "Luz Natural de Janela": "soft natural window lighting, gentle falloff, realistic ambient indoor light",
    "Nenhum (Padrão do Estilo)": "",
}

CREATIVE_FREEDOM_LEVELS = {
    "Equilibrado (Recomendado: Rosto idêntico + liberdade artística)": {"control_scale": 0.50, "cfg": 7.0},
    "Fiel / Estrito (Mantém roupas e postura quase idênticas)": {"control_scale": 0.78, "cfg": 6.5},
    "Máxima Imaginação (Roupas novas, cenários fantásticos, efeitos)": {"control_scale": 0.38, "cfg": 7.8},
}

ASPECT_RATIOS = {
    "Retrato / Vertical (896 x 1152) [Ideal para Pessoas]": (896, 1152),
    "Quadrado (1024 x 1024) [Padrão Redes Sociais]": (1024, 1024),
    "Paisagem / Horizontal (1152 x 896) [Cinema e Ambientes]": (1152, 896),
}


def enhance_prompt_magic(prompt: str) -> str:
    """Enriquece prompts curtos de forma transparente para atingir padrão de estúdio."""
    cleaned = prompt.strip()
    if not cleaned:
        return "masterpiece, sharp focus, ultra-detailed subject, high-end photography"

    # Se for uma descrição curta (menos de 6 palavras), adiciona polimento
    words = cleaned.split()
    if len(words) < 8:
        return f"{cleaned}, highly detailed, sharp facial features, natural lighting, professional quality"
    return cleaned


def apply_style_and_lighting(
    style_name: str,
    lighting_name: str,
    prompt: str,
    negative_prompt: str,
    magic_enabled: bool = True,
):
    preset = STYLE_PRESETS.get(style_name, STYLE_PRESETS["Livre (Sem estilo predefinido)"])

    base_prompt = enhance_prompt_magic(prompt) if magic_enabled else prompt.strip()
    lighting_tag = LIGHTING_MOODS.get(lighting_name, "")

    parts = [preset["prompt_prefix"], base_prompt]
    if lighting_tag:
        parts.append(f", {lighting_tag}")
    parts.append(preset["prompt_suffix"])

    final_prompt = "".join(parts).strip()

    if negative_prompt and negative_prompt.strip():
        final_neg = f"{negative_prompt.strip()}{preset['negative_suffix']}"
    else:
        final_neg = preset["negative_suffix"].lstrip(", ")

    return final_prompt, final_neg, preset["folder"]
