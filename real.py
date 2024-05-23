import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {"success": True, "error": None, "transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def translate_text(text, target_lang):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text


def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")


def main():
    st.title("Speech-to-Speech Translation")

    st.write("Select the source language and target language.")
    source_lang = st.selectbox("Source Language", ["en", "es", "fr", "de", "zh-cn"])
    target_lang = st.selectbox("Target Language", ["en", "es", "fr", "de", "zh-cn"])

    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        st.write("Recording...")

        result = recognize_speech_from_mic(recognizer, microphone)
        if result["transcription"]:
            st.write("You said: {}".format(result["transcription"]))

            translated_text = translate_text(result["transcription"], target_lang)
            st.write("Translated text: {}".format(translated_text))

            text_to_speech(translated_text, target_lang)
            st.audio("output.mp3")
        else:
            if result["error"]:
                st.write("ERROR: {}".format(result["error"]))


if __name__ == "__main__":
    main()
