from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import whisper
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

model = whisper.load_model("base")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        result = model.transcribe(audio_path)
        user_prompt = result["text"]
    except Exception as e:
        os.remove(audio_path)
        return JSONResponse(
            content={"error": f"Transcription failed: {str(e)}"}, status_code=500
        )

    os.remove(audio_path)

    try:
        gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = gemini_model.generate_content(user_prompt)
        return JSONResponse(
            content={"transcription": user_prompt, "gemini_response": response.text}
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Gemini request failed: {str(e)}"}, status_code=500
        )
