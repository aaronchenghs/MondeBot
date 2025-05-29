from googletrans import Translator

translator = Translator()

def translate_to_target_language(text: str, target_language: str) -> str | None:
    try:
        result = translator.translate(text, dest=target_language)
        if result.src != target_language:
            return result.text
        else:
            return None
    except Exception as e:
        print(f"[Translation Error]: {e}")
        return None
