from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env vars
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

# List and print available models
models = genai.list_models()
for model in models:
    print(f"{model.name} — {model.description}")
