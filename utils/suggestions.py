import os
from openai import OpenAI

from utils.constants import GPT_MODEL


def query_suggestions(original_text: str, language_code: str) -> list[str]:
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Moved inside function

        prompt = (
            f"Twitch Chat Message: {original_text}\n"
            f"Reply casually like a twitch-conscious Brazilian-American 23 yr old "
            f"Suggest 2 things to say back in {language_code}, with English in parentheses."
        )

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=120,
            frequency_penalty=0.2,
        )

        content = response.choices[0].message.content
        suggestions = content.strip().split('\n')
        return [s.strip('- ').strip() for s in suggestions if s.strip()]

    except Exception as e:
        print(f"❌ Error getting suggestions: {e}")
        return []
