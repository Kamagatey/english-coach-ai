import edge_tts
import asyncio
import os
import re
import streamlit as st

VOICE_EN = "en-US-GuyNeural"
AUDIO_FILE = "last_response.mp3"

async def generate_voice(text):
    # On sépare pour ne garder que l'anglais
    parts = re.split(r'EXPLICATION:', text, flags=re.IGNORECASE)
    english_part = parts[0].strip()
    
    if english_part:
        if os.path.exists(AUDIO_FILE):
            try: os.remove(AUDIO_FILE)
            except: pass
        
        # Génération du fichier audio réaliste
        communicate = edge_tts.Communicate(english_part, VOICE_EN)
        await communicate.save(AUDIO_FILE)
        return True
    return False

def speak(text):
    """Génère l'audio et l'affiche dans Streamlit avec lecture automatique"""
    if asyncio.run(generate_voice(text)):
        play_audio_file()

def play_audio_file():
    """Utilise Streamlit pour envoyer le son au navigateur (PC ou Téléphone)"""
    if os.path.exists(AUDIO_FILE):
        # On utilise st.audio avec autoplay pour que le son sorte sur ton téléphone
        st.audio(AUDIO_FILE, format="audio/mp3", autoplay=True)