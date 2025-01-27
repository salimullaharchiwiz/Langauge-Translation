import speech_recognition as spr
from googletrans import Translator
import streamlit as st
import asyncio

# Creating Recogniser() class object
recog1 = spr.Recognizer()

# Function to capture voice and recognize text
def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for background noise
        audio = recog.listen(source)  # Capture audio input
        recognized_text = recog.recognize_google(audio)  # Recognize using Google's recognizer
        return recognized_text.lower()
    except spr.UnknownValueError:
        return None
    except spr.RequestError as e:
        return None

# Async function for translation
async def translate_text(text, src_lang, target_lang):
    translator = Translator()
    try:
        result = await translator.translate(text, src=src_lang, dest=target_lang)
        return result.text
    except Exception as e:
        st.error(f"An error occurred during translation: {e}")
        return None

# Streamlit app setup
st.title("Voice Translator App")
st.write("Select the translation direction and speak or type your text!")

# Option to choose translation direction
translation_direction = st.radio("Choose translation direction:", ["English to Pashto", "Pashto to English"])

# Option to choose voice or text input
input_method = st.radio("Choose your input method:", ["Voice", "Text"])

# Initialize session state for button label
if "button_label" not in st.session_state:
    st.session_state.button_label = "🎤 Record Voice"

# Functionality for voice input
if input_method == "Voice":
    st.write("Click the microphone below and speak.")
    
    # Button that changes text between "Record" and "Recording..."
    record_button = st.button(st.session_state.button_label)
    
    # If the button is clicked, change its label to "Recording..."
    if record_button:
        st.session_state.button_label = "Recording..."
        with spr.Microphone() as source:
            st.info("Listening...")

            MyText = recognize_speech(recog1, source)

            if MyText:
                st.success("Audio recorded successfully!")
                st.success(f"You said: {MyText}")

                # Translate based on selected translation direction
                if translation_direction == "English to Pashto":
                    translated_text = asyncio.run(translate_text(MyText, src_lang="en", target_lang="ps"))
                elif translation_direction == "Pashto to English":
                    translated_text = asyncio.run(translate_text(MyText, src_lang="ps", target_lang="en"))

                if translated_text:
                    st.success(f"Translated: {translated_text}")
            else:
                st.error("Could not recognize your voice. Please try again.")
        
        # After recording, reset the button label back to "Record Voice"
        st.session_state.button_label = "🎤 Record Voice"

# Functionality for text input
elif input_method == "Text":
    user_text = st.text_area("Type your text below:", height=100)

    if st.button("Translate"):
        if user_text:
            # Translate based on selected translation direction
            if translation_direction == "English to Pashto":
                translated_text = asyncio.run(translate_text(user_text, src_lang="en", target_lang="ps"))
            elif translation_direction == "Pashto to English":
                translated_text = asyncio.run(translate_text(user_text, src_lang="ps", target_lang="en"))

            st.success(f"Translated: {translated_text}")
        else:
            st.warning("Please enter text to translate.")