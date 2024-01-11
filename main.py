import streamlit as st
import google.generativeai as genai
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="EDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# Configure the generative AI API key
genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")  # Replace with your actual API key

# Load the generative model
@st.cache_resource
def load_model() -> genai.GenerativeModel:
    model = genai.GenerativeModel('gemini-pro')
    return model

# Start the chat session
if 'chat' not in st.session_state:
    st.session_state.chat = load_model().start_chat(history=[])

# Chat session storage
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = []

# Main chat logic
prompt = st.text_area("Ask a question:")

if st.button("Ask"):
    if prompt:
        # Append user's message to chat session
        st.session_state.chat_session.append({'user': {'role': 'user', 'parts': [prompt]}})

        # Get the model's response
        response = st.session_state.chat.send_message(prompt)

        # Append model's response to chat session
        st.session_state.chat_session.append({'user': {'role': 'model', 'parts': [response.text]}})

# Display chat history
for message in st.session_state.chat_session:
    role, parts = message['user']['role'], message['user']['parts']
    with st.expander(f"{role.capitalize()} says:"):
        st.write(parts[0])  # Assuming only text for simplicity
