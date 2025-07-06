from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"

def translate_to_target_language(text: str, target_language: str) -> str | None:
    try:
        detected_lang = detect_language(text)
        if detected_lang != target_language:
            return GoogleTranslator(source='auto', target=target_language).translate(text)
        return None
    except Exception as e:
        print(f"[Translation Error]: {e}")
        return None
