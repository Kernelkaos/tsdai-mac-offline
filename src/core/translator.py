# Offline rule-based translation dictionary for common Brazilian Portuguese concepts to English SDXL terms

PT_TO_EN_DICTIONARY = {
    # Poses e ângulos
    "de costas": "from behind, back view",
    "costas": "back view",
    "meio perfil": "half profile, semi-profile",
    "perfil": "profile view",
    "de frente": "front view, facing camera",
    "olhando para camera": "looking at camera",
    "corpo inteiro": "full body shot",
    "plano inteiro": "full body shot",
    "meio corpo": "medium shot, waist up",
    "close": "close-up shot",
    "sentada": "sitting",
    "sentado": "sitting",
    "em pe": "standing",
    "de pe": "standing",
    "andando": "walking",
    "sorrindo": "smiling, gentle smile",
    "sorriso": "gentle smile",
    
    # Sujeitos
    "mulher": "woman",
    "homem": "man",
    "garota": "young woman",
    "garoto": "young man",
    "pessoa": "person",
    "modelo": "fashion model",
    
    # Roupas e trajes
    "biquini fio dental": "thong bikini, swimwear",
    "biquini": "bikini, stylish swimwear",
    "maiô": "one-piece swimsuit",
    "maio": "one-piece swimsuit",
    "terno": "tailored suit",
    "vestido": "elegant dress",
    "jaqueta de couro": "leather jacket",
    "roupa casual": "casual modern clothes",
    "roupas casuais": "casual modern clothes",
    "roupa de banho": "swimwear",
    "sem camisa": "shirtless",
    
    # Cabelos e caracteristicas
    "morena": "brunette hair",
    "loira": "blonde hair",
    "ruiva": "red hair",
    "cabelo longo": "long hair",
    "cabelos longos": "long hair",
    "cabelo curto": "short hair",
    "cabelo cacheado": "curly hair",
    "cabelos cacheados": "curly hair",
    "cabelo crespo": "afro textured hair",
    "olhos castanhos": "brown eyes",
    "olhos azuis": "blue eyes",
    "olhos verdes": "green eyes",
    "brasileira": "brazilian",
    "brasileiro": "brazilian",
    
    # Cenários
    "praia": "tropical beach, ocean in background",
    "piscina": "luxury swimming pool",
    "estudio": "photo studio",
    "cidade": "urban street",
    "quarto": "modern bedroom",
    "natureza": "outdoor nature scenery",
    "jardim": "lush garden",
}

def translate_pt_to_en(text: str) -> str:
    """Translates common Portuguese keywords to English photography terms offline."""
    if not text:
        return ""
    
    lower_text = text.lower()
    
    # Substitui expressões compostas primeiro (mais longas)
    sorted_pairs = sorted(PT_TO_EN_DICTIONARY.items(), key=lambda x: len(x[0]), reverse=True)
    
    translated = lower_text
    for pt_term, en_term in sorted_pairs:
        if pt_term in translated:
            translated = translated.replace(pt_term, en_term)
            
    return translated
