import os
import speech_recognition as sr
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash-lite")
chat = model.start_chat()
recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Couldn’t understand.")
            return ""
        except sr.RequestError as e:
            print(f"Speech API error: {e}")
            return ""


def chat_with_gemini(prompt):
    response = chat.send_message(prompt)
    return response.text


while True:
    user_input = listen()
    if user_input.lower() in ["quit", "stop"]:
        print("Exiting.")
        break
    if user_input:
        reply = chat_with_gemini(user_input)
        print(f"Gemini: {reply}")
