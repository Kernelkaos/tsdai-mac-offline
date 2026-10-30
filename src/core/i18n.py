# Multilingual localization dictionaries (English & Portuguese-BR)

TRANSLATIONS = {
    "pt_BR": {
        "title": "🎨 Tsdai — Transformador de Imagens com IA (Mac Offline)",
        "subtitle": (
            "Transforme qualquer foto com inteligência artificial profissional (SDXL + IP-Adapter + ControlNet). "
            "100% privado, offline e otimizado para a memória unificada do seu Mac.\n"
            "As imagens são salvas automaticamente em `Imagens/Tsdai_Outputs/` organizadas por estilo."
        ),
        "source_image": "1. Escolha a Foto Original (Identidade & Postura)",
        "style_preset": "2. Estilo Visual",
        "style_info": "Define o acabamento estético e a categoria da pasta onde a imagem será salva.",
        "aspect_ratio": "3. Proporção da Imagem (Aspect Ratio)",
        "aspect_info": "Encaixa a imagem de forma inteligente no enquadramento sem esticar nem deformar.",
        "lighting_mood": "4. Iluminação & Atmosfera",
        "lighting_info": "Adiciona iluminação fotográfica natural sem estourar as cores da pele.",
        "creative_mode": "5. Nível de Liberdade Criativa & Roupas",
        "creative_info": "Escolha se deseja trocar de roupa mantendo a mesma pessoa, ou manter as roupas originais.",
        "prompt": "6. O que você quer ver? (Prompt Principal)",
        "prompt_placeholder": "Ex: ela de meio perfil, de costas, olhando para a camera sorrindo e de biquíni...",
        "magic_prompt": "✨ Varinha Mágica (Traduzir termos para estúdio fotográfico e enriquecer detalhes)",
        "magic_info": "Traduz termos em português (ex: 'de biquíni', 'sorrindo') para a linguagem técnica do SDXL.",
        "neg_prompt": "O que EVITAR na imagem (Opcional)",
        "neg_placeholder": "Ex: óculos, roupas pesadas, fundo escuro, pessoas no fundo...",
        "adv_accordion": "⚙️ Controles Avançados: Identidade vs. Postura & Roupa (Opcional)",
        "ip_adapter_label": "Fidelidade da Identidade / Rosto (LoRA Instantânea IP-Adapter: 0.80)",
        "ip_adapter_info": (
            "0.75–0.85: Mantém o rosto, sorriso, olhos e cabelos idênticos à pessoa original sem treinar LoRA."
        ),
        "control_scale_label": "Fidelidade da Pose e Silhueta (ControlNet Canny: 0.35)",
        "control_scale_info": (
            "0.30–0.40: Perfeito para trocar de roupa mantendo a pose; 0.70+: Força a mesma roupa original."
        ),
        "guidance_end_label": "Momento de Liberação das Roupas (Término da Guia: 0.35)",
        "guidance_end_info": (
            "0.35: Mantém postura inicial e libera para desenhar biquíni/roupas novas; 1.0: Mantém roupas originais."
        ),
        "steps_label": "Medidor de Passos de Renderização (35 = Equilíbrio Rápido e Nítido)",
        "steps_info": "25–35: Rápido e realista | 40–50: Qualidade máxima de textura | 60+: Risco de saturação",
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
        "footer_title": "💡 Como o Tsdai Garante Identidade Real e Troca de Roupas sem Caricatura",
        "footer_ip_adapter": (
            "* **LoRA Instantânea de Identidade (IP-Adapter Face):** Você não precisa gastar tempo treinando LoRA nem "
            "ajustando pesos manualmente. O modelo analisa a fisionomia, sorriso, cor de pele, sardas e formato dos "
            "cabelos da foto enviada e transfere para a nova imagem em alta definição."
        ),
        "footer_clothes": (
            "* **Como Trocar Roupas Mantendo a Pose:** Fotos com bermudas ou camisetas criam linhas nos contornos. "
            "Ao selecionar o modo **'Troca de Roupa'**, o sistema usa a pose nos primeiros 35% do processo para "
            "fixar a curvatura do corpo e a postura, e depois libera a IA para desenhar o biquíni ou traje novo com "
            "pele natural, sem ser presa aos cortes do tecido anterior."
        ),
        "footer_proportions": (
            "* **Enquadramento e Proporção sem Esticar:** O enquadramento inteligente utiliza o método proporcional "
            "Lanczos no centro da imagem. Isso impede que a modelo pareça mais baixa, espremida ou com membros "
            "desproporcionais."
        ),
        "footer_colors": (
            "* **Cores Naturais vs. Caricatura (CFG 5.0):** Em vez de usar saturações exageradas (como 7.5 ou 8.0) que "
            "transformam fotos em desenhos plásticos, o sistema opera calibrado em **5.0**, entregando luz suave, pele "
            "fotoestática e sombras reais de estúdio fotográfico."
        ),
        "footer_apple": (
            "* **100% Offline no Mac M1 Max:** Processamento local no chip Apple Silicon Metal (MPS), "
            "garantindo privacidade absoluta e velocidade sem depender de nuvem."
        ),
        "error_no_image": "Por favor, selecione ou arraste uma foto original primeiro.",
        "error_no_prompt": "Por favor, digite o que gostaria de ver na foto ou selecione um estilo.",
    },
    "en_US": {
        "title": "🎨 Tsdai — AI Image Transformer (Mac Offline)",
        "subtitle": (
            "Transform any photo using professional artificial intelligence (SDXL + IP-Adapter + ControlNet). "
            "100% private, offline, and optimized for Apple Silicon unified memory.\n"
            "Images are automatically cataloged into `~/Pictures/Tsdai_Outputs/` by style."
        ),
        "source_image": "1. Source Input Photo (Identity & Posture)",
        "style_preset": "2. Visual Style Preset",
        "style_info": "Defines aesthetic styling and creates dedicated output folders.",
        "aspect_ratio": "3. Image Proportions (Aspect Ratio)",
        "aspect_info": "Intelligently fits the image into the frame without stretching or distortion.",
        "lighting_mood": "4. Lighting & Mood Atmosphere",
        "lighting_info": "Applies natural photographic studio lighting without oversaturating skin tones.",
        "creative_mode": "5. Creative Freedom & Clothing Level",
        "creative_info": "Choose whether to change clothing preserving identity, or preserve original clothes.",
        "prompt": "6. What would you like to see? (Core Prompt)",
        "prompt_placeholder": "E.g., woman from behind, semi-profile, smiling at camera, wearing a bikini...",
        "magic_prompt": "✨ Magic Prompt (Translate to studio terms & enrich details)",
        "magic_info": "Translates Portuguese terms into native SDXL prompt syntax.",
        "neg_prompt": "Things to AVOID (Optional Negative Prompt)",
        "neg_placeholder": "E.g., glasses, heavy clothes, dark background, extra limbs...",
        "adv_accordion": "⚙️ Advanced Parameters: Identity vs. Posture & Clothing (Optional)",
        "ip_adapter_label": "Identity Likeness (Instant LoRA IP-Adapter: 0.80)",
        "ip_adapter_info": (
            "0.75–0.85: Preserves exact facial likeness, smile, and hair without manual LoRA training."
        ),
        "control_scale_label": "Posture & Silhouette Scale (ControlNet Canny: 0.35)",
        "control_scale_info": (
            "0.30–0.40: Perfect for clothing swaps; 0.70+: Strictly locks original clothes."
        ),
        "guidance_end_label": "Clothing Release Transition (Guidance End: 0.35)",
        "guidance_end_info": (
            "0.35: Locks posture then releases contours for bikini/new clothes; 1.0: Keeps original clothes."
        ),
        "steps_label": "Inference Steps Gauge (35 = Studio Sweet Spot)",
        "steps_info": "25–35: Fast & realistic | 40–50: Maximum texture detail | 60+: Over-baking risk",
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
        "footer_title": "💡 How Tsdai Guarantees Real Identity & Clothing Swaps Without Distortion",
        "footer_ip_adapter": (
            "* **Instant Identity LoRA (IP-Adapter Face):** No need to train a LoRA. The model extracts facial "
            "features, smile, skin tone, freckles, and curly hair from the source photo and injects them in HD."
        ),
        "footer_clothes": (
            "* **Changing Outfits While Preserving Posture:** Using the 'Clothing Swap' preset guides the pose during "
            "the first 35% of steps, then releases edge contours to let the model render a bikini or new outfit."
        ),
        "footer_proportions": (
            "* **Smart Proportional Framing:** Uses Lanczos center-fitting to prevent stretching or unnatural scaling."
        ),
        "footer_colors": (
            "* **Natural Colors vs. Caricature (CFG 5.0):** Calibrated at 5.0 for realistic skin tones and soft light."
        ),
        "footer_apple": (
            "* **100% Offline on Apple Silicon:** Fully local execution on M1 Max with MPS acceleration."
        ),
        "error_no_image": "Please upload an input photo first.",
        "error_no_prompt": "Please describe what you would like to see or pick a style preset.",
    },
}


def get_text(lang: str, key: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["pt_BR"])
    return lang_dict.get(key, TRANSLATIONS["en_US"].get(key, key))
