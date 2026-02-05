import google.generativeai as genai
import os
from dotenv import load_dotenv



# On précise le nom du fichier ici
load_dotenv(dotenv_path="config.env") 

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class EnglishCoach:
    def __init__(self, model_name='gemini-2.5-flash-lite'):
        self.system_instruction = (
            "You are a professional English coach. Follow this structure for EVERY response:\n"
            "1. Start with your response in English ONLY.\n"
            "2. If needed, add a section starting exactly with 'EXPLICATION:' followed by your French comments.\n"
            "3. Correct grammar mistakes in brackets [like this].\n"
            "4. We can talk about any topic."
        )
        self.set_model(model_name)

    def set_model(self, model_name):
        """Permet de changer le modèle sans perdre l'historique"""
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        # On garde l'historique de conversation si on change de modèle
        if not hasattr(self, 'chat'):
            self.chat = self.model.start_chat(history=[])

    def send_message(self, text):
        full_query = f"{self.system_instruction}\nUser says: {text}"
        try:
            response = self.chat.send_message(full_query)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "ERROR_QUOTA: Désolé, ce modèle est épuisé. Changez de modèle dans le menu à gauche !"
            return f"ERREUR: {str(e)}"