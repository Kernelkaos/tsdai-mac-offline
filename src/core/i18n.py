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
        "aspect_info": "Encaixa a imagem de forma inteligente no enquadramento sem esticar nem deformar.",
        "lighting_mood": "4. Iluminação & Atmosfera",
        "lighting_info": "Adiciona iluminação fotográfica natural sem estourar as cores da pele.",
        "creative_mode": "5. Nível de Liberdade Criativa da IA",
        "creative_info": "Equilibrado: mantém fisionomia e postura com anatomia real.",
        "prompt": "6. O que você quer ver? (Prompt Principal)",
        "prompt_placeholder": "Ex: mulher de costas, biquíni na praia tropical, mar ao fundo...",
        "magic_prompt": "✨ Varinha Mágica (Traduzir para termos de estúdio e enriquecer detalhes)",
        "magic_info": "Traduz termos em português (ex: 'de costas', 'biquíni') para a linguagem técnica do SDXL.",
        "neg_prompt": "O que EVITAR na imagem (Opcional)",
        "neg_placeholder": "Ex: óculos, chapéu, fundo escuro, pessoas no fundo...",
        "adv_accordion": "⚙️ Configurações Avançadas de Qualidade (Opcional)",
        "steps_label": "Medidor de Passos de Renderização (43 = Equilíbrio Perfeito de Estúdio)",
        "steps_info": "20–30: Rápido | 43: Qualidade Máxima de Estúdio | 55+: Risco de saturação/queima",
        "control_scale_label": "Aderência Fina aos Contornos (0.65 = Equilíbrio Anatômico)",
        "control_scale_info": "0.60–0.75: Preserva proporções humanas reais | Abaixo de 0.50: Risco de deformação",
        "cfg_label": "Fidelidade ao Texto / CFG (5.0 = Cores e Tons de Pele Naturais)",
        "cfg_info": "Valores entre 4.5 e 5.5 geram pele realista. Acima de 7.0 as cores estouram como pintura.",
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
        "footer_title": "💡 Como Obter Resultados Naturais e Sem Deformações (Guia Rápido)",
        "footer_steps": (
            "* **Passos (43):** O número ideal para SDXL. Garante textura de pele, cabelos e tecidos com nitidez."
        ),
        "footer_freedom": (
            "* **Fidelidade Anatômica (0.65 - 0.85):** Para fotos de pessoas ou roupas, mantenha a aderência aos "
            "contornos em **0.65 ou mais**. Se diminuir abaixo de 0.50, a IA tentará 'adivinhar' a pose e o corpo "
            "pode ficar com braços ou costas desproporcionais."
        ),
        "footer_cfg": (
            "* **Cores Reais vs. Caricatura (CFG 4.5 a 5.5):** O controle CFG foi calibrado em **5.0**. Valores mais "
            "altos forçam laranjas e vermelhos agressivos que parecem pintura a óleo; valores em torno de 5.0 entregam "
            "a luz suave e natural de uma câmera fotográfica profissional."
        ),
        "footer_aspect": (
            "* **Encaixe Inteligente (Proporção):** O sistema agora corta e ajusta a imagem de forma inteligente "
            "no centro sem jamais espremer ou esticar a sua foto original."
        ),
        "footer_memory": (
            "* **Aceleração Apple Silicon:** O programa roda direto na GPU do M1 Max com até 80% da memória "
            "unificada, de forma 100% offline e privada."
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
        "aspect_ratio": "3. Image Proportions (Aspect Ratio)",
        "aspect_info": "Intelligently fits the image into the frame without stretching or distortion.",
        "lighting_mood": "4. Lighting & Mood Atmosphere",
        "lighting_info": "Applies natural photographic studio lighting without oversaturating skin tones.",
        "creative_mode": "5. AI Creative Freedom Level",
        "creative_info": "Balanced: preserves likeness and posture with authentic human anatomy.",
        "prompt": "6. What would you like to see? (Core Prompt)",
        "prompt_placeholder": "E.g., woman from behind, bikini on tropical beach, ocean in background...",
        "magic_prompt": "✨ Magic Prompt (Translate to studio terms & enrich details)",
        "magic_info": "Translates Portuguese terms into native SDXL prompt syntax.",
        "neg_prompt": "Things to AVOID (Optional Negative Prompt)",
        "neg_placeholder": "E.g., glasses, hats, dark background, extra limbs...",
        "adv_accordion": "⚙️ Advanced Parameters & Edge Preview (Optional)",
        "steps_label": "Inference Steps Gauge (43 = Studio Sweet Spot)",
        "steps_info": "20–30: Fast drafts | 43: Studio Render Master | 55+: Over-baking risks",
        "control_scale_label": "Contour Edge Rigidity (0.65 = Anatomical Realism)",
        "control_scale_info": "0.60–0.75: Preserves true human proportions | Below 0.50: Risk of distortion",
        "cfg_label": "Text Guidance Scale / CFG (5.0 = Natural Skin Tones)",
        "cfg_info": "Values between 4.5 and 5.5 produce realistic skin. Values above 7.0 look artificial.",
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
        "footer_title": "💡 How to Achieve Natural & Proportional Results (Quick Guide)",
        "footer_steps": (
            "* **Inference Steps (43):** Ideal for SDXL. Ensures skin texture, hair, and cloth details are razor sharp."
        ),
        "footer_freedom": (
            "* **Anatomical Fidelity (0.65 - 0.85):** Keep edge adherence at **0.65 or higher**. "
            "Dropping below 0.50 forces the AI to hallucinate poses, often distorting limbs or anatomy."
        ),
        "footer_cfg": (
            "* **True Colors vs. Over-Saturated Caricature (CFG 4.5 to 5.5):** CFG is calibrated at **5.0**. "
            "Higher values force harsh orange/red tones like thick oil paint; ~5.0 yields soft, realistic light."
        ),
        "footer_aspect": (
            "* **Smart Fit Proportions:** Intelligently centers and crops the image without stretching."
        ),
        "footer_memory": (
            "* **Apple Silicon Architecture:** Runs directly on the M1 Max GPU using unified memory, 100% offline."
        ),
        "error_no_image": "Please upload an input photo first.",
        "error_no_prompt": "Please describe what you would like to see or pick a style preset.",
    },
}


def get_text(lang: str, key: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["pt_BR"])
    return lang_dict.get(key, TRANSLATIONS["en_US"].get(key, key))
