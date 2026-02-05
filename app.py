import streamlit as st
from brain import EnglishCoach
from audio_engine import speak, play_audio_file
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

st.set_page_config(page_title="Coach Multi-Modèles", layout="centered")

# --- INITIALISATION (CORRECTION) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- BARRE LATÉRALE : SÉLECTION DU MODÈLE ---
with st.sidebar:
    st.title("⚙️ Réglages")
    model_choice = st.selectbox(
        "Choisir le modèle :",
        [
            "gemini-2.5-flash-lite", 
            "gemini-2.5-flash", 
            "gemini-2.0-flash", 
            "gemini-3-flash-preview"
        ],
        index=0,
        help="Si un modèle affiche une erreur de quota (429), changez-le ici."
    )

# Initialisation du coach avec le modèle choisi
if "coach" not in st.session_state:
    st.session_state.coach = EnglishCoach(model_choice)

# Si l'utilisateur change de modèle dans le menu, on met à jour le coach
if st.session_state.coach.model_name != model_choice:
    st.session_state.coach.set_model(model_choice)
    st.sidebar.success(f"Modèle changé pour : {model_choice}")

# --- RESTE DE L'INTERFACE ---
st.title("🎓 English Coach")

# Historique
chat_placeholder = st.container()
for msg in st.session_state.messages:
    with chat_placeholder.chat_message(msg["role"]):
        st.write(msg["content"])

# --- INPUTS ---
user_input = None
st.write("---")
cols = st.columns([1, 1, 2])

with cols[0]:
    audio_data = mic_recorder(start_prompt="🎤 Parler", stop_prompt="🛑 Stop", key='recorder')

with cols[1]:
    if st.button("🔊 Replay"):
        play_audio_file()

# Gestion de l'audio (Transcription)
if audio_data and 'bytes' in audio_data:
    with st.spinner("Transcription..."):
        transcriber = genai.GenerativeModel(model_choice)
        try:
            res = transcriber.generate_content([
                "Return only the transcription of this audio.",
                {"mime_type": "audio/wav", "data": audio_data['bytes']}
            ])
            user_input = res.text
        except Exception as e:
            st.error("Erreur de quota sur ce modèle. Changez-le à gauche.")

# Saisie texte
text_input = st.chat_input("Écris ici...")
if text_input: user_input = text_input

# Réponse
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_placeholder.chat_message("user"):
        st.write(user_input)

    with chat_placeholder.chat_message("assistant"):
        response = st.session_state.coach.send_message(user_input)
        
        if "ERROR_QUOTA" in response:
            st.error(response)
        else:
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            speak(response)