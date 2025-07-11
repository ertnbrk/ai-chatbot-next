from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from chatbot import OpenAIChatbot
from pydantic import BaseModel
from speech_processor import SpeechProcessor
import os

# Create temp_audio folder if it does not exist
if not os.path.exists("temp_audio"):
    os.makedirs("temp_audio")
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


chatbot = OpenAIChatbot()

class ChatRequest(BaseModel):
    message: str
    lang: str = "en"  # Default language is English

@app.post("/chat")
async def chat(request: ChatRequest):
    return {"reply": chatbot.generate_response(request.message, request.lang)}


@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    """Converts user's voice to text, sends it to the chatbot, and returns the response as audio."""
    try:
        file_location = f"temp_audio/{file.filename}"
        
        # Save the audio file
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Transcribe audio to text using Whisper API
        transcribed_text = SpeechProcessor.transcribe_audio(file_location)

        # Send the text to the chatbot and get a response
        response_text = chatbot.generate_response(transcribed_text, lang="tr")

        # Convert the response to speech
        audio_path = SpeechProcessor.text_to_speech(response_text, lang="tr")

        if not audio_path:
            return {"error": "Audio file could not be created."}

        return FileResponse(audio_path, media_type="audio/mpeg", filename="response.mp3")

    except Exception as e:
        print(f" Error: {e}")
        return {"error": "500 Internal Server Error", "message": str(e)}