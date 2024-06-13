import streamlit as st
import requests

st.title("Sentiment Analysis Web Application")
text_input = st.text_area("Enter text for analysis:")
if st.button("Analyze"):
    response = requests.post("http://localhost:8000/process_text", json={"text": text_input})
    result = response.json()
    st.write(f"Sentiment: {result['sentiment']}")
    st.write(f"Score: {result['score']}")