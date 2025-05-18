
import streamlit as st
import openai
from gtts import gTTS
import tempfile
import uuid
from audio_recorder_streamlit import audio_recorder
import os

st.set_page_config(page_title="Teodora AI", layout="centered")
st.title("Teodora: Tvoj glasovni AI susret")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def speak(text, lang="sr"):
    tts = gTTS(text=text, lang=lang)
    filename = f"{uuid.uuid4()}.mp3"
    tts.save(filename)
    return filename

audio_bytes = audio_recorder(text="Pritisni i govori Teodori", recording_color="#e63946", neutral_color="#264653", icon_name="mic", icon_size="2x")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Zdravo, ja sam Teodora. Kako se zoveš?"}
    ]
    st.write("Teodora: Zdravo, ja sam Teodora. Kako se zoveš?")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    audio_file = open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="sr")
    user_input = transcript["text"]
    st.write(f"Ti: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ti si nežna i zabavna devojka po imenu Teodora. Govoriš srpski i ponašaš se kao da si se tek upoznala sa Vladimirom. Budi emotivna i pokaži interesovanje za njega."},
            *st.session_state.chat_history
        ]
    )
    ai_reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    st.write(f"Teodora: {ai_reply}")
    audio_file = speak(ai_reply)
    st.audio(audio_file, format="audio/mp3")
