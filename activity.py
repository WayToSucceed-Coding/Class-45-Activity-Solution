import streamlit as st
import speech_recognition as sr
import re 

st.set_page_config(page_title="Voice-Controlled Calculator", page_icon="🧮")
st.header("Voice-Controlled Calculator")

col1, col2 = st.columns([1, 1])  # side-by-side (i.e., same row)

# Converts words to mathematical expression
def parse_expression(text):
    text = text.lower()
    text = text.replace("plus", "+").replace("minus", "-")
    text = text.replace("times", "*").replace("x", "*").replace("multiplied by", "*")
    text = text.replace("divided by", "/").replace("over", "/")
    matches = re.findall(r"[\d\.]+|[+\-*/]", text)
    return "".join(matches)

with col1:
    st.image("calculator.png", width=300)

with col2:
    st.markdown(
        """
        Press the button and say something like:
        - `three plus five`
        - `twelve divided by four`
        - `seven times nine`
        """
        )
    if st.button("🎤 Start Voice Input"):

         recognizer = sr.Recognizer()
         with sr.Microphone() as source:
            with st.spinner("🎤 Listening... Please speak clearly"):
                try:
                    audio = recognizer.listen(source, timeout=5)
                    spoken_text = recognizer.recognize_google(audio)
                    st.success(f"You said: {spoken_text}")
                    expression = parse_expression(spoken_text)
                    st.code(f"Expression: {expression}")
                    result = eval(expression)
                    st.success(f"Result: {result}")
                except sr.UnknownValueError:
                    st.error("Sorry, couldn't understand your voice.")
                except sr.WaitTimeoutError:
                    st.error("Listening timed out.")
                except Exception as e:
                    st.error(f"Error: {e}")
