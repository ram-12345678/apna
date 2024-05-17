import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Supported languages
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Telugu": "te",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur"
}

# Streamlit app layout
st.title("Speech-to-Speech Translation")
st.write("Select the source and target languages, then speak or type to translate.")

src_lang = st.selectbox("Source Language", list(languages.keys()))
target_lang = st.selectbox("Target Language", list(languages.keys()))

# Radio buttons to choose input method
input_method = st.radio("Choose input method:", ("Microphone", "Text Input"))

if input_method == "Microphone":
    if st.button("Start Translation with Microphone"):
        st.write("Please speak into your microphone...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=languages[src_lang])
            st.write(f"Recognized Text: {text}")

            translated = translator.translate(text, src=languages[src_lang], dest=languages[target_lang])
            translated_text = translated.text
            st.write(f"Translated Text: {translated_text}")

            tts = gTTS(text=translated_text, lang=languages[target_lang])
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)

            st.audio(audio_file, format='audio/mp3')

            os.remove(audio_file)
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            st.write(f"An error occurred: {e}")

elif input_method == "Text Input":
    text_input = st.text_area("Enter text to translate")
    if st.button("Translate Text"):
        try:
            translated = translator.translate(text_input, src=languages[src_lang], dest=languages[target_lang])
            translated_text = translated.text
            st.write(f"Translated Text: {translated_text}")

            tts = gTTS(text=translated_text, lang=languages[target_lang])
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)

            st.audio(audio_file, format='audio/mp3')

            os.remove(audio_file)
        except Exception as e:
            st.write(f"An error occurred: {e}")
