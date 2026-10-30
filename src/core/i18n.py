# Multilingual localization dictionaries (English & Portuguese-BR)

TRANSLATIONS = {
    "pt_BR": {
        "title": "🎨 Tsdai — Transformador de Imagens com IA (Mac Offline)",
        "subtitle": (
            "Transforme qualquer foto com inteligência artificial profissional (SDXL + ControlNet). "
            "100% privado, offline e otimizado para a memória unificada do seu Mac.\n"
            "As imagens são salvas automaticamente em `Imagens/Tsdai_Outputs/` organizadas por estilo."
        ),
        "source_image": "1. Escolha a Foto Original",
        "style_preset": "2. Estilo Visual",
        "style_info": "Define o acabamento estético e a categoria da pasta onde a imagem será salva.",
        "aspect_ratio": "3. Proporção da Imagem (Aspect Ratio)",
        "aspect_info": "Escolha o formato correto para não esticar ou deformar o assunto da foto.",
        "lighting_mood": "4. Iluminação & Atmosfera",
        "lighting_info": "Adiciona a iluminação profissional perfeita sem precisar digitar prompts complexos.",
        "creative_mode": "5. Nível de Liberdade Criativa da IA",
        "creative_info": "Controla o quanto a IA pode inventar roupas, cabelos e cenários novos mantendo o rosto.",
        "prompt": "6. O que você quer ver? (Prompt Principal)",
        "prompt_placeholder": "Ex: mulher com terno moderno de veludo, fundo de estúdio desfocado...",
        "magic_prompt": "✨ Varinha Mágica (Enriquecer detalhes automaticamente)",
        "magic_info": "Transforma descrições simples em prompts profissionais detalhados.",
        "neg_prompt": "O que EVITAR na imagem (Opcional)",
        "neg_placeholder": "Ex: óculos, relógio, fundo escuro, pessoas no fundo...",
        "adv_accordion": "⚙️ Configurações Avançadas de Qualidade (Opcional)",
        "steps_label": "Medidor de Passos de Renderização (43 = Equilíbrio Perfeito de Estúdio)",
        "steps_info": "20–30: Rápido | 43: Qualidade Máxima de Estúdio | 55+: Risco de saturação/queima",
        "control_scale_label": "Aderência Fina aos Contornos (0.50 = Equilíbrio Natural)",
        "control_scale_info": "0.35–0.50: Roupas e cabelos novos | 0.70–0.85: Mantém roupas idênticas",
        "cfg_label": "Fidelidade ao Texto / CFG (7.0 = Cores Naturais)",
        "cfg_info": "Valores muito altos podem forçar cores excessivamente saturadas.",
        "canny_low": "Sensibilidade do Contorno (Baixo)",
        "canny_high": "Sensibilidade do Contorno (Alto)",
        "seed_label": "Semente Numérica (-1 para Aleatório)",
        "preview_btn": "🔍 Ver Contornos que a IA enxerga (Instantâneo)",
        "generate_btn": "🚀 Gerar Imagem com Qualidade Máxima",
        "output_image": "Imagem Final Gerada",
        "canny_preview": "Linhas Guia Detectadas (Esqueleto do Contorno)",
        "status_title": "Status do Sistema",
        "status_ready": "Pronto para criar. Seus arquivos serão salvos em ~/Pictures/Tsdai_Outputs/",
        "saved_prefix": "✓ Imagem salva em:",
        "footer_title": "💡 Guia Intuitivo de Criatividade e Qualidade",
        "footer_steps": (
            "* **Passos (43):** O algoritmo limpa o ruído gradualmente. 43 passos garante nitidez máxima em "
            "texturas de pele, fios de cabelo e tecidos sem queimar a imagem."
        ),
        "footer_freedom": (
            "* **Liberdade Criativa:** No modo *Equilibrado*, a IA preserva a fisionomia e a postura da pessoa, "
            "mas tem total liberdade para desenhar novas roupas, iluminação realista e cenários envolventes."
        ),
        "footer_aspect": (
            "* **Proporção da Imagem:** Use sempre *Retrato (Vertical)* para pessoas e *Paisagem (Cinema)* "
            "para ambientes amplos, evitando que a pessoa fique esticada ou achatada."
        ),
        "footer_memory": (
            "* **Tecnologia Apple Silicon:** Utiliza até 80% da memória unificada (64 GB) em velocidade "
            "máxima, sem precisar de internet nem arriscar travar o seu Mac."
        ),
        "error_no_image": "Por favor, selecione ou arraste uma foto original primeiro.",
        "error_no_prompt": "Por favor, digite o que gostaria de ver na foto ou selecione um estilo.",
    },
    "en_US": {
        "title": "🎨 Tsdai — AI Image Transformer (Mac Offline)",
        "subtitle": (
            "Transform any photo using professional artificial intelligence (SDXL + ControlNet). "
            "100% private, offline, and optimized for Apple Silicon unified memory.\n"
            "Images are automatically cataloged into `~/Pictures/Tsdai_Outputs/` by style."
        ),
        "source_image": "1. Source Input Photo",
        "style_preset": "2. Visual Style Preset",
        "style_info": "Defines aesthetic styling and creates dedicated output folders.",
        "aspect_ratio": "3. Aspect Ratio (Proportions)",
        "aspect_info": "Select the natural orientation to prevent subject distortion or stretching.",
        "lighting_mood": "4. Lighting & Mood Atmosphere",
        "lighting_info": "Applies professional photographic lighting without complex prompt syntax.",
        "creative_mode": "5. AI Creative Freedom Level",
        "creative_info": "Controls how freely the AI can design new clothing and scenery while preserving the face.",
        "prompt": "6. What would you like to see? (Core Prompt)",
        "prompt_placeholder": "E.g., woman in a stylish velvet blazer, soft studio bokeh...",
        "magic_prompt": "✨ Magic Prompt (Auto-enrich detail & textures)",
        "magic_info": "Automatically turns brief descriptions into high-end studio prompts.",
        "neg_prompt": "Things to AVOID (Optional Negative Prompt)",
        "neg_placeholder": "E.g., glasses, hats, dark background, extra limbs...",
        "adv_accordion": "⚙️ Advanced Parameters & Edge Preview (Optional)",
        "steps_label": "Inference Steps Gauge (43 = Studio Sweet Spot)",
        "steps_info": "20–30: Fast drafts | 43: Studio Render Master | 55+: Over-baking risks",
        "control_scale_label": "Contour Edge Rigidity (0.50 = Optimal Balance)",
        "control_scale_info": "0.35–0.50: Allows new clothes & natural light | 0.70–0.85: Rigid structural lock",
        "cfg_label": "Text Guidance Scale / CFG (7.0 = Realistic Color Range)",
        "cfg_info": "Higher values enforce strict prompt adherence but may oversaturate colors.",
        "canny_low": "Canny Low Threshold",
        "canny_high": "Canny High Threshold",
        "seed_label": "Seed Number (-1 for Random)",
        "preview_btn": "🔍 Preview Edge Skeleton (Instant)",
        "generate_btn": "🚀 Transform Image with Peak Quality",
        "output_image": "Final Generated Output",
        "canny_preview": "Detected Edge Skeleton (ControlNet Input)",
        "status_title": "System Status",
        "status_ready": "Ready. Images will be automatically exported to ~/Pictures/Tsdai_Outputs/",
        "saved_prefix": "✓ Saved to:",
        "footer_title": "💡 Intuitive Quality & Performance Guide",
        "footer_steps": (
            "* **Inference Steps (43):** Progressively removes noise. 43 steps guarantees maximum texture "
            "definition (skin pores, hair strands, fabric weave) without contrast burning."
        ),
        "footer_freedom": (
            "* **Creative Freedom:** In *Balanced* mode, the AI maintains facial resemblance and posture "
            "while synthesizing realistic lighting, fresh wardrobe, and cinematic backdrops."
        ),
        "footer_aspect": (
            "* **Aspect Ratio (Proportions):** Always pick *Portrait (Vertical)* for people and *Landscape (Cinema)* "
            "for wide scenes to prevent subject distortion."
        ),
        "footer_memory": (
            "* **Apple Silicon Architecture:** Utilizes up to 80% of your unified memory (64 GB) at maximum "
            "throughput, completely air-gapped without risk of system freezes."
        ),
        "error_no_image": "Please upload an input photo first.",
        "error_no_prompt": "Please describe what you would like to see or pick a style preset.",
    },
}

def get_text(lang: str, key: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["pt_BR"])
    return lang_dict.get(key, TRANSLATIONS["en_US"].get(key, key))
