import edge_tts
import asyncio
import os
import re
import streamlit as st
import time

VOICE_EN = "en-US-GuyNeural"

async def generate_voice(text):
    parts = re.split(r'EXPLICATION:', text, flags=re.IGNORECASE)
    english_part = parts[0].strip()
    
    if english_part:
        # On crée un nom unique avec le timestamp pour forcer le téléphone à charger le nouveau son
        filename = f"resp_{int(time.time())}.mp3"
        
        # Nettoyage : on supprime les anciens fichiers mp3 du dossier pour ne pas encombrer
        for f in os.listdir():
            if f.startswith("resp_") and f.endswith(".mp3"):
                try: os.remove(f)
                except: pass
        
        communicate = edge_tts.Communicate(english_part, VOICE_EN)
        await communicate.save(filename)
        return filename
    return None

def speak(text):
    # On récupère le nom du nouveau fichier créé
    filename = asyncio.run(generate_voice(text))
    if filename:
        # On stocke le nom dans la session pour que le bouton Replay le retrouve
        st.session_state.last_audio_file = filename
        st.audio(filename, format="audio/mp3", autoplay=True)

def play_audio_file():
    # Rejoue le dernier fichier généré
    if "last_audio_file" in st.session_state:
        if os.path.exists(st.session_state.last_audio_file):
            st.audio(st.session_state.last_audio_file, format="audio/mp3", autoplay=True)