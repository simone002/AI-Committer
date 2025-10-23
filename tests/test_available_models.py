import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configura l'API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY non trovata!")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Modelli disponibili con la tua API key:\n")

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display name: {model.display_name}")
            print(f"   Supported methods: {model.supported_generation_methods}")
            print()
except Exception as e:
    print(f"❌ Errore durante il recupero dei modelli: {e}")
    print("\nProva a verificare:")
    print("1. Che la tua API key sia valida")
    print("2. Che tu abbia abilitato l'API Gemini nel tuo progetto Google Cloud")
    print("3. Visita: https://makersuite.google.com/app/apikey")