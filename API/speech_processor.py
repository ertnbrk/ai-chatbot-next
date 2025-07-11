import openai
import os


class SpeechProcessor:
    """Speech recognition with OpenAI Whisper API and speech generation with OpenAI TTS."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found! Please check your environment variables.")
        openai.api_key = self.api_key  # Set the API key

    @staticmethod
    def transcribe_audio(file_path: str) -> str:
        """Converts an audio file to text (using Whisper API)."""
        try:
            with open(file_path, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return response.text

        except openai.OpenAIError as e:
            print(f" OpenAI Whisper API Error: {e}")
            return " Speech recognition failed."

        except Exception as e:
            print(f" General Error: {e}")
            return "⚠️ An error occurred."
    @staticmethod
    def text_to_speech(text: str, lang: str = "tr") -> str:
        """Converts text to speech using OpenAI TTS API and saves it as a file."""
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",  # One of OpenAI's voice models
                input=text
            )

            file_path = f"temp_audio/response.mp3"
            with open(file_path, "wb") as audio_file:
                audio_file.write(response.content)  # Save the response as MP3

            return file_path  # Return the file path

        except openai.OpenAIError as e:
            print(f"OpenAI TTS API Error: {e}")
            return None  # Do not return audio file if there is an error

        except Exception as e:
            print(f"General TTS Error: {e}")
            return None
