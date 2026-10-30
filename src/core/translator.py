# Offline rule-based translation dictionary for Brazilian Portuguese concepts to English SDXL terms

PT_TO_EN_DICTIONARY = {
    # Poses, ângulos e expressões
    "olhando para a câmera sorrindo": "looking at camera smiling warmly, happy smile",
    "olhando para a camera sorrindo": "looking at camera smiling warmly, happy smile",
    "olhando para a câmera": "looking at camera",
    "olhando para a camera": "looking at camera",
    "olhando para camera": "looking at camera",
    "meio perfil de costas": "semi-profile from behind, looking over shoulder",
    "meio perfil": "semi-profile",
    "de meio perfil": "semi-profile",
    "de costas": "from behind, back view",
    "costas": "back view",
    "de frente": "front view, facing camera",
    "perfil": "profile view",
    "sorrindo": "smiling, warm gentle smile",
    "sorriso": "warm gentle smile",
    "corpo inteiro": "full body shot",
    "plano inteiro": "full body shot",
    "meio corpo": "medium shot, waist up",
    "close-up": "close-up portrait",
    "close": "close-up portrait",
    "sentada": "sitting comfortably",
    "sentado": "sitting comfortably",
    "em pé": "standing pose",
    "em pe": "standing pose",
    "de pé": "standing pose",
    "de pe": "standing pose",
    "andando": "walking naturally",

    # Vestimentas e estilos
    "de biquíni": "wearing a stylish bikini, swimwear",
    "de biquini": "wearing a stylish bikini, swimwear",
    "biquíni": "bikini swimwear",
    "biquini": "bikini swimwear",
    "biquíni de praia": "beach bikini swimwear",
    "biquini de praia": "beach bikini swimwear",
    "maiô": "one-piece swimsuit",
    "maio": "one-piece swimsuit",
    "roupa de banho": "swimwear",
    "terno": "tailored suit",
    "vestido": "elegant dress",
    "jaqueta de couro": "leather jacket",
    "roupa casual": "casual modern clothes",
    "sem camisa": "shirtless",

    # Fisionomia e características físicas
    "brasileira": "Brazilian woman",
    "brasileiro": "Brazilian man",
    "mulher": "woman",
    "homem": "man",
    "morena": "brunette hair, tanned skin",
    "loira": "blonde hair",
    "ruiva": "red hair",
    "cabelos cacheados": "curly hair, long curly locks",
    "cabelo cacheado": "curly hair, long curly locks",
    "cabelo crespo": "afro textured curly hair",
    "cabelo longo": "long hair",
    "cabelos longos": "long hair",
    "cabelo curto": "short hair",
    "olhos castanhos": "brown eyes",
    "olhos verdes": "green eyes",
    "olhos azuis": "blue eyes",
    "pele morena": "warm tanned glowing skin",
    "sardas": "freckles on cheeks",
    "tatuagem no braço": "detailed arm tattoo",
    "tatuagem": "tattoo",

    # Cenários
    "praia tropical": "tropical sandy beach, palm trees and ocean",
    "praia": "beach, ocean waves and sand",
    "piscina": "luxury resort swimming pool",
    "pôr do sol": "sunset golden hour",
    "por do sol": "sunset golden hour",
    "estúdio": "photo studio",
    "estudio": "photo studio",
    "cidade": "urban street",
    "natureza": "scenic nature landscape",
    "jardim": "lush green garden",
}


def translate_pt_to_en(text: str) -> str:
    """Translates common Portuguese keywords to English photography terms offline."""
    if not text:
        return ""

    lower_text = text.lower()

    # Substitui expressões mais longas primeiro
    sorted_pairs = sorted(PT_TO_EN_DICTIONARY.items(), key=lambda x: len(x[0]), reverse=True)

    translated = lower_text
    for pt_term, en_term in sorted_pairs:
        if pt_term in translated:
            translated = translated.replace(pt_term, en_term)

    return translated
