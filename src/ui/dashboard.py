import json
from datetime import datetime
from pathlib import Path

import gradio as gr
from PIL import Image

from src.core.engine import ImageTransformerEngine, InsufficientMemoryError
from src.core.i18n import get_text
from src.core.memory import get_memory_info
from src.core.styles import (
    ASPECT_RATIOS,
    CREATIVE_FREEDOM_LEVELS,
    LIGHTING_MOODS,
    STYLE_PRESETS,
    apply_style_and_lighting,
)

OUTPUT_BASE_DIR = Path.home() / "Pictures" / "Tsdai_Outputs"


def save_output_image(image: Image.Image, style_folder: str, metadata: dict) -> Path:
    target_dir = OUTPUT_BASE_DIR / style_folder
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seed = metadata.get("seed", "rand")
    filename_img = f"img_{timestamp}_s{seed}.png"
    filename_meta = f"img_{timestamp}_s{seed}.json"

    img_path = target_dir / filename_img
    meta_path = target_dir / filename_meta

    image.save(img_path, format="PNG")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return img_path


def create_dashboard(engine: ImageTransformerEngine):
    current_lang = "pt_BR"

    def t(key: str) -> str:
        return get_text(current_lang, key)

    def preview_canny(image, low_thresh, high_thresh, aspect_choice):
        if image is None:
            raise gr.Error(t("error_no_image"))
        target_size = ASPECT_RATIOS.get(aspect_choice, (896, 1152))
        return engine.process_canny_image(image, int(low_thresh), int(high_thresh), target_size=target_size)

    def on_freedom_change(freedom_choice):
        params = CREATIVE_FREEDOM_LEVELS.get(freedom_choice, {"control_scale": 0.65, "cfg": 5.0})
        return params["control_scale"], params["cfg"]

    def run_inference(
        image,
        prompt,
        neg_prompt,
        style_choice,
        aspect_choice,
        lighting_choice,
        freedom_choice,
        magic_enabled,
        steps,
        guidance,
        control_scale,
        low_thresh,
        high_thresh,
        seed,
    ):
        if image is None:
            raise gr.Error(t("error_no_image"))

        styled_prompt, styled_neg, style_folder = apply_style_and_lighting(
            style_name=style_choice,
            lighting_name=lighting_choice,
            prompt=prompt or "",
            negative_prompt=neg_prompt or "",
            magic_enabled=magic_enabled,
        )
        actual_seed = int(seed)
        target_size = ASPECT_RATIOS.get(aspect_choice, (896, 1152))

        try:
            output = engine.generate(
                input_image=image,
                prompt=styled_prompt,
                negative_prompt=styled_neg,
                steps=int(steps),
                guidance_scale=float(guidance),
                controlnet_scale=float(control_scale),
                low_threshold=int(low_thresh),
                high_threshold=int(high_thresh),
                seed=actual_seed,
                target_size=target_size,
            )
        except InsufficientMemoryError as e:
            raise gr.Error(str(e)) from e

        metadata = {
            "timestamp": datetime.now().isoformat(),
            "style_preset": style_choice,
            "lighting_mood": lighting_choice,
            "creative_freedom": freedom_choice,
            "aspect_ratio": aspect_choice,
            "dimensions": f"{target_size[0]}x{target_size[1]}",
            "magic_prompt_active": magic_enabled,
            "user_prompt": prompt,
            "final_prompt": styled_prompt,
            "final_negative_prompt": styled_neg,
            "steps": int(steps),
            "guidance_scale": float(guidance),
            "controlnet_scale": float(control_scale),
            "low_threshold": int(low_thresh),
            "high_threshold": int(high_thresh),
            "seed": actual_seed,
            "device": engine.device,
        }
        saved_path = save_output_image(output, style_folder, metadata)

        info = get_memory_info()
        status = (
            f"{t('saved_prefix')} {saved_path.parent.name}/{saved_path.name} ({target_size[0]}x{target_size[1]})\n"
            f"Hardware: {info['device']} | Alocado: {info['allocated_mb']} MB | Cache: {info['cached_mb']} MB"
        )
        return output, status

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=("ui-sans-serif", "system-ui", "sans-serif"),
        font_mono=("ui-monospace", "Menlo", "monospace"),
    ).set(
        button_primary_background_fill="*primary_500",
        button_primary_background_fill_hover="*primary_600",
        button_primary_text_color="white",
    )

    with gr.Blocks(title="Tsdai — Transformador de Imagens com IA", analytics_enabled=False) as interface:
        gr.Markdown(
            f"""
            # {t('title')}
            {t('subtitle')}
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(label=t("source_image"), type="pil")

                with gr.Row():
                    style_choice = gr.Dropdown(
                        label=t("style_preset"),
                        choices=list(STYLE_PRESETS.keys()),
                        value="Retrato Fotográfico de Estúdio",
                        info=t("style_info"),
                        scale=1,
                    )
                    aspect_choice = gr.Dropdown(
                        label=t("aspect_ratio"),
                        choices=list(ASPECT_RATIOS.keys()),
                        value="Retrato / Vertical (896 x 1152) [Ideal para Pessoas]",
                        info=t("aspect_info"),
                        scale=1,
                    )

                with gr.Row():
                    lighting_choice = gr.Dropdown(
                        label=t("lighting_mood"),
                        choices=list(LIGHTING_MOODS.keys()),
                        value="Natural Suave de Estúdio (Softbox)",
                        info=t("lighting_info"),
                        scale=1,
                    )
                    freedom_choice = gr.Dropdown(
                        label=t("creative_mode"),
                        choices=list(CREATIVE_FREEDOM_LEVELS.keys()),
                        value="Equilibrado (Recomendado: Rosto/Postura idênticos + Realismo)",
                        info=t("creative_info"),
                        scale=1,
                    )

                prompt = gr.Textbox(
                    label=t("prompt"),
                    placeholder=t("prompt_placeholder"),
                    lines=2,
                )

                magic_toggle = gr.Checkbox(
                    label=t("magic_prompt"),
                    value=True,
                    info=t("magic_info"),
                )

                neg_prompt = gr.Textbox(
                    label=t("neg_prompt"),
                    placeholder=t("neg_placeholder"),
                    lines=1,
                )

                with gr.Accordion(t("adv_accordion"), open=False):
                    steps = gr.Slider(
                        minimum=10,
                        maximum=100,
                        step=1,
                        value=43,
                        label=t("steps_label"),
                        info=t("steps_info"),
                    )
                    control_scale = gr.Slider(
                        minimum=0.0,
                        maximum=2.0,
                        step=0.05,
                        value=0.65,
                        label=t("control_scale_label"),
                        info=t("control_scale_info"),
                    )
                    guidance = gr.Slider(
                        minimum=1.0,
                        maximum=20.0,
                        step=0.5,
                        value=5.0,
                        label=t("cfg_label"),
                        info=t("cfg_info"),
                    )
                    with gr.Row():
                        low_thresh = gr.Slider(minimum=1, maximum=255, step=1, value=100, label=t("canny_low"))
                        high_thresh = gr.Slider(minimum=1, maximum=255, step=1, value=200, label=t("canny_high"))
                    seed = gr.Number(value=-1, precision=0, label=t("seed_label"))

                    preview_canny_btn = gr.Button(t("preview_btn"), variant="secondary")

                generate_btn = gr.Button(t("generate_btn"), variant="primary", size="lg")

            with gr.Column(scale=1):
                output_image = gr.Image(label=t("output_image"), type="pil")
                canny_preview = gr.Image(label=t("canny_preview"), type="pil")
                status_box = gr.Textbox(
                    label=t("status_title"),
                    value=t("status_ready"),
                    interactive=False,
                    lines=2,
                )

        gr.Markdown(
            f"""
            ---
            ### {t('footer_title')}
            {t('footer_steps')}
            {t('footer_freedom')}
            {t('footer_cfg')}
            {t('footer_aspect')}
            {t('footer_memory')}
            """
        )

        freedom_choice.change(
            fn=on_freedom_change,
            inputs=[freedom_choice],
            outputs=[control_scale, guidance],
        )

        preview_canny_btn.click(
            fn=preview_canny,
            inputs=[input_image, low_thresh, high_thresh, aspect_choice],
            outputs=[canny_preview],
        )

        generate_btn.click(
            fn=run_inference,
            inputs=[
                input_image,
                prompt,
                neg_prompt,
                style_choice,
                aspect_choice,
                lighting_choice,
                freedom_choice,
                magic_toggle,
                steps,
                guidance,
                control_scale,
                low_thresh,
                high_thresh,
                seed,
            ],
            outputs=[output_image, status_box],
        )

    interface.launch_theme = theme
    return interface
