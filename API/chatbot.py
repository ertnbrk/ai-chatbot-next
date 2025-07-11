import openai
import os

class OpenAIChatbot:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(" OPENAI_API_KEY bulunamadı!")
        openai.api_key = self.api_key  

    def generate_response(self, message: str, lang: str = "en") -> str:
        try:
            response = openai.chat.completions.create(  
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are smart ai assistant"},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
            )

            reply = response.choices[0].message.content  

            # Eğer hedef dil İngilizce değilse çeviri yap
            if lang != "en":
                reply = self.translate(reply, target=lang)

            return reply

        except openai.OpenAIError as e:
            print(f"OpenAI API Hatası: {e}")
            return f"OpenAI API hatası: {str(e)}"

        except Exception as e:
            print(f"Genel Hata: {e}")
            return f"Genel hata: {str(e)}"

    def translate(self, text: str, target: str) -> str:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Lütfen bu metni {target} diline çevir."},
                    {"role": "user", "content": text}
                ]
            )

            return response.choices[0].message.content  # Çeviri sonucunu döndür

        except openai.OpenAIError as e:
            print(f" Çeviri API Hatası: {e}")
            return text  # Çeviri başarısız olursa orijinal metni döndür

        except Exception as e:
            print(f" Genel Çeviri Hatası: {e}")
            return text  # Hata durumunda metni değiştirme
