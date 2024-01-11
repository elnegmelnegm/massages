import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Set page configuration
st.set_page_config(
    page_title="EDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

st.markdown('''
<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)

st.markdown('''
Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Configure the generative AI API key
genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")  # Replace with your actual API key

# Load the generative model
@st.cache_resource
def load_model() -> genai.GenerativeModel:
    model = genai.GenerativeModel('gemini-pro')
    return model

# Function to scrape text from the specified URL using BeautifulSoup
def scrape_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant text content, modify as needed based on the site's structure
    text_content = ""
    for paragraph in soup.find_all('p'):
        text_content += paragraph.get_text() + "\n"

    return text_content

# Start the chat session
if 'chat' not in st.session_state:
    st.session_state.chat = load_model().start_chat(history=[])

# Chat session storage
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = []

# List of URLs to scrape data from
urls = [
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2023/",
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2021/",
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2022/",
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2023/",
    # Add other URLs here
]

# Scrape data from each URL and append to text_content
text_content = ""
for url in urls:
    text_content += scrape_text(url)

# Display scraped text
st.write("Text content from the specified URLs:")
st.write(text_content)

# Ask a question based on the combined text
prompt = st.text_area("Ask a question based on the combined text:")

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
