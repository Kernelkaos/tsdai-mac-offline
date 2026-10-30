# Presets de estilos, iluminação, liberdade criativa e enriquecedor de prompts

from src.core.translator import translate_pt_to_en

STYLE_PRESETS = {
    "Retrato Fotográfico de Estúdio": {
        "folder": "studio_portrait",
        "prompt_prefix": "award-winning photographic portrait of ",
        "prompt_suffix": (
            ", 85mm portrait lens, balanced natural lighting, "
            "sharp focus, natural realistic skin texture, highly detailed, raw photo, realistic shadows"
        ),
        "negative_suffix": (
            ", airbrushed, plastic skin, oversaturated, shiny skin, "
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
    "Golden Hour (Luz Dourada de Entardecer)": "natural warm golden hour light, soft rim lighting, warm glow",
    "Natural Suave de Estúdio (Softbox)": "soft diffused studio lighting, gentle ambient light, flattering exposure",
    "Luz Natural de Janela": "soft natural window lighting, gentle realistic falloff, natural indoor ambiance",
    "Cinematográfica Moody": "subtle moody cinematic lighting, natural shadows, controlled contrast",
    "Neon Sutil / Cyberpunk": "subtle neon ambient highlights, cyan and warm tones, realistic street reflection",
    "Nenhum (Iluminação Natural da Foto)": "",
}

CREATIVE_FREEDOM_LEVELS = {
    "Troca de Roupa (Recomendado para biquíni / novo look mantendo o rosto e postura)": {
        "ip_scale": 0.80,
        "control_scale": 0.35,
        "guidance_end": 0.35,
        "cfg": 5.0,
    },
    "Equilibrado (Mantém a pessoa e silhueta com boa liberdade de cena)": {
        "ip_scale": 0.80,
        "control_scale": 0.50,
        "guidance_end": 0.60,
        "cfg": 5.0,
    },
    "Fiel Extremo (Mesma roupa original, contornos e proporções idênticos)": {
        "ip_scale": 0.85,
        "control_scale": 0.80,
        "guidance_end": 1.0,
        "cfg": 4.5,
    },
    "Criativo / Reinterpretação (Nova pose artística com a mesma fisionomia)": {
        "ip_scale": 0.70,
        "control_scale": 0.20,
        "guidance_end": 0.25,
        "cfg": 5.5,
    },
}

ASPECT_RATIOS = {
    "Vertical Retrato Cheio (768 x 1344) [Ideal para Corpo Inteiro / Stories]": (768, 1344),
    "Retrato / Vertical (896 x 1152) [Ideal para Meio Corpo e Retrato]": (896, 1152),
    "Quadrado (1024 x 1024) [Padrão Feed Redes Sociais]": (1024, 1024),
    "Paisagem / Horizontal (1152 x 896) [Cinema e Ambientes]": (1152, 896),
}


def enhance_prompt_magic(prompt: str) -> str:
    """Enriquece prompts sem forçar termos conflitantes."""
    cleaned = prompt.strip()
    if not cleaned:
        return "natural realistic photography, sharp focus, professional quality"

    lower = cleaned.lower()
    additions = []

    # Se o prompt menciona biquíni ou maiô, ajuda a remover roupas pesadas
    if any(k in lower for k in ["biquini", "bikini", "maiô", "maio", "swimwear"]):
        additions.append("bare back, bare legs, fit athletic body")

    if any(k in lower for k in ["costas", "behind", "back"]):
        additions.append("looking over shoulder, realistic posture")

    extra = ", ".join(additions)
    if extra:
        return f"{cleaned}, {extra}, natural skin texture, master photography"
    return f"{cleaned}, natural skin texture, realistic posture, master photography"


def apply_style_and_lighting(
    style_name: str,
    lighting_name: str,
    prompt: str,
    negative_prompt: str,
    magic_enabled: bool = True,
) -> tuple[str, str, str]:
    """Combina o prompt do usuário, tradução, enriquecimento mágico e presets de iluminação/estilo."""
    style = STYLE_PRESETS.get(style_name, STYLE_PRESETS["Retrato Fotográfico de Estúdio"])
    lighting_desc = LIGHTING_MOODS.get(lighting_name, "")

    user_text = translate_pt_to_en(prompt)
    if magic_enabled:
        user_text = enhance_prompt_magic(user_text)

    # Injeta a iluminação se presente
    if lighting_desc:
        user_text = f"{user_text}, {lighting_desc}"

    final_prompt = f"{style['prompt_prefix']}{user_text}{style['prompt_suffix']}".strip()
    user_neg = translate_pt_to_en(negative_prompt)

    # Se o usuário pediu biquíni, adicionar roupas do dia a dia no negative prompt automaticamente
    extra_neg = ""
    if any(k in prompt.lower() for k in ["biquini", "bikini", "maiô", "maio"]):
        extra_neg = ", t-shirt, shorts, cotton clothing, crop top, oversized clothes, pants, bermuda"

    final_negative = f"{user_neg}{extra_neg}{style['negative_suffix']}".strip().lstrip(", ")

    return final_prompt, final_negative, style["folder"]
