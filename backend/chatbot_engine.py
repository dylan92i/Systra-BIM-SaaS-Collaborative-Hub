import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

DEMO_RESPONSES = {
    "combien de murs": "🔍 Analyse BIM (Mode Démo) : J'ai détecté 45 murs dans la maquette IFC, dont 12 murs porteurs en béton armé.",
    "surface totale": "📏 Analyse BIM (Mode Démo) : La surface totale des planchers est de 1250 m².",
    "défauts": "⚠️ Analyse BIM (Mode Démo) : 3 clashs détectés entre le réseau CVC et la structure au niveau R+2."
}

def get_response(user_input):
    """
    Main entry point for Chatbot.
    Hybrid Logic: Real AI if available, else Fallback Demo.
    """
    user_input_lower = user_input.lower()
    
    # 1. Mode Démo / Fallback Simulation (Checks for missing key)
    if not API_KEY or API_KEY == "TODO" or "demo" in API_KEY.lower():
         # Simulation logic requested: returning simulation response without crashing
        return _get_demo_response(user_input_lower)
        
    # 2. Real AI
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        print(f"⚠️ API Error: {e}. Switching to Demo Mode.")
        return _get_demo_response(user_input_lower)

def _get_demo_response(text):
    for key, response in DEMO_RESPONSES.items():
        if key in text:
            return response
    
    return "🤖 Mode Démo : Je suis une simulation. Posez-moi des questions sur les 'murs', la 'surface', ou les 'défauts' pour voir mes capacités BIM."
