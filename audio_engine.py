import edge_tts
import asyncio
import os
import re
import streamlit as st

# Configuration de la voix et du fichier
VOICE_EN = "en-US-GuyNeural"
AUDIO_FILE = "last_response.mp3"

async def generate_voice(text):
    """
    Sépare le texte pour ne garder que la partie anglaise et génère le fichier MP3.
    """
    # On sépare pour ne garder que ce qui précède 'EXPLICATION:'
    parts = re.split(r'EXPLICATION:', text, flags=re.IGNORECASE)
    english_part = parts[0].strip()
    
    if english_part:
        # On supprime l'ancien fichier s'il existe pour éviter les conflits
        if os.path.exists(AUDIO_FILE):
            try:
                os.remove(AUDIO_FILE)
            except:
                pass
        
        # Génération de l'audio avec edge-tts
        communicate = edge_tts.Communicate(english_part, VOICE_EN)
        await communicate.save(AUDIO_FILE)
        return True
    return False

def speak(text):
    """
    Fonction principale appelée par l'interface pour générer et lire le son.
    """
    if asyncio.run(generate_voice(text)):
        play_audio_file()

def play_audio_file():
    """
    Affiche le composant audio Streamlit. 
    L'option autoplay=True permet la lecture automatique sur le navigateur.
    """
    if os.path.exists(AUDIO_FILE):
        # Le format audio/mp3 est universellement supporté par iOS et Android
        st.audio(AUDIO_FILE, format="audio/mp3", autoplay=True)