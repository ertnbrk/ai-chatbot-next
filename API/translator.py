from deep_translator import GoogleTranslator
from langdetect import detect
import openai

class Translator:
    """Structure that provides better translation support."""

    @staticmethod
    def detect_language(text: str) -> str:
        try:
            detected_lang = detect(text)
            return detected_lang
        except Exception as e:
            print(f"⚠️ Language detection error: {e}")
            return "en"

    @staticmethod
    def translate(text: str, source: str, target: str) -> str:
        if source == target:
            return text  # Do not translate to the same language
        
        try:
            return GoogleTranslator(source=source, target=target).translate(text)
        except Exception as e:
            print(f"⚠️ Google Translate error: {e}. Trying with OpenAI API...")
            return Translator.openai_translate(text, target)

    @staticmethod
    def openai_translate(text: str, target: str) -> str:
        """If Google Translate fails, translate using OpenAI ChatGPT."""
        openai.api_key = "YOUR_OPENAI_API_KEY"  # API KEY should be added here or set in environment variables
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not found! Please check your environment variables.")
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Please translate this text to {target}."},
                {"role": "user", "content": text}
            ]
        )
        return response["choices"][0]["message"]["content"]
