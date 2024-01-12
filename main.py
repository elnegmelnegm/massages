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
    st.session_state.chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])

# Chat session storage
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = []

# List of URLs to scrape data from
urls = [
    "https://edaegypt.gov.eg/ar/%D8%A7%D9%84%D8%AF%D8%B3%D8%AA%D9%88%D8%B1-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A6%D9%8A-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A/%D8%A7%D9%84%D8%A7%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%B4%D8%A7%D8%A6%D8%B9%D8%A9/",
    "https://edaegypt.gov.eg/ar/%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D8%A7%D8%B9%D9%84%D8%A7%D9%85%D9%89/%D8%A7%D9%84%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/%D8%B1%D8%A6%D9%8A%D8%B3-%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9-%D9%8A%D8%B1%D8%A3%D8%B3-%D8%A7%D8%AC%D8%AA%D9%85%D8%A7%D8%B9%D9%8A-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A7%D8%AA-%D9%88%D8%A7%D9%84%D8%AC%D9%87%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D8%A7%D9%84%D8%B1%D9%82%D8%A7%D8%A8%D9%8A%D8%A9-%D8%B9%D9%84%D9%89-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D9%88%D8%A7%D9%84%D9%84%D8%AC%D9%86%D8%A9-%D8%A7%D9%84%D9%81%D9%86%D9%8A%D8%A9-%D8%A7%D9%84%D8%B9%D9%84%D9%8A%D8%A7-%D9%84%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A/",
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2022/",
    "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/2023/",
    "https://edaegypt.gov.eg/media/smoeouq1/ca-of-pharmaceutical-care-faq-faq-for-public.pdf",
    "https://edaegypt.gov.eg/media/i4jeg1oh/%D8%A7%D9%84%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%A3%D9%83%D8%AB%D8%B1-%D8%B4%D9%8A%D9%88%D8%B9%D8%A7-%D8%AD%D9%88%D9%84-%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%A5%D8%B9%D8%AA%D9%85%D8%A7%D8%AF-%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D9%85%D8%B9%D8%A7%D9%85%D9%84-%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%AC%D9%88%D8%AF%D8%A9-%D8%A8%D8%B4%D8%B1%D9%83%D8%A7%D8%AA-%D8%A7%D9%84%D8%A3%D8%AF%D9%88%D9%8A%D8%A9.pdf",
    "https://edaegypt.gov.eg/media/10xnmimk/%D8%A7%D9%84%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%A3%D9%83%D8%AB%D8%B1-%D8%B4%D9%8A%D9%88%D8%B9%D8%A7-%D8%AD%D9%88%D9%84-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A5%D8%B9%D8%AA%D9%85%D8%A7%D8%AF-%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9-%D9%84%D9%84%D9%85%D9%88%D8%A7%D8%AF-%D8%A7%D9%84%D9%82%D9%8A%D8%A7%D8%B3%D9%8A%D8%A9.pdf",
    "https://edaegypt.gov.eg/media/ezcdaok0/%D8%A7%D9%84%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%A3%D9%83%D8%AB%D8%B1-%D8%B4%D9%8A%D9%88%D8%B9%D8%A7-%D8%AD%D9%88%D9%84-%D8%A7%D9%84%D9%81%D8%AD%D8%B5-%D9%88-%D8%A7%D9%84%D8%AA%D8%AD%D9%84%D9%8A%D9%84.pdf",
    "https://edaegypt.gov.eg/media/3oppdnjz/insert-faqs-09-21.pdf",
    "https://edaegypt.gov.eg/ar/%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D8%A7%D8%B9%D9%84%D8%A7%D9%85%D9%89/%D8%A7%D9%84%D8%A5%D8%B9%D9%84%D8%A7%D9%86%D8%A7%D8%AA/%D8%AF%D9%84%D9%8A%D9%84-%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%A7%D9%84%D8%AA%D8%AF%D8%B1%D9%8A%D8%A8%D9%8A%D8%A9-%D9%84%D8%B4%D9%87%D8%B1-%D9%8A%D9%86%D8%A7%D9%8A%D8%B1-%D9%A2%D9%A0%D9%A2%D9%A4-%D8%A7%D9%84%D9%85%D9%82%D8%AF%D9%85%D8%A9-%D9%85%D9%86-%D9%85%D8%B1%D9%83%D8%B2-%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9-%D9%84%D9%84%D8%AA%D8%B7%D9%88%D9%8A%D8%B1-%D8%A7%D9%84%D9%85%D9%87%D9%86%D9%89-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D9%85%D8%B1/",
    "https://edaegypt.gov.eg/ar/%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D8%A7%D8%B9%D9%84%D8%A7%D9%85%D9%89/%D8%A7%D9%84%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/%D8%B1%D8%A6%D9%8A%D8%B3-%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%A1-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9-%D9%8A%D8%B3%D8%AA%D9%82%D8%A8%D9%84-%D9%88%D9%81%D8%AF%D8%A7-%D9%85%D9%86-%D9%87%D9%8A%D8%A6%D8%A9-%D8%AA%D9%86%D8%B8%D9%8A%D9%85-%D8%A7%D9%84%D8%A3%D8%AF%D9%88%D9%8A%D8%A9-%D8%A8%D8%AC%D9%85%D9%87%D9%88%D8%B1%D9%8A%D8%A9-%D8%A7%D9%84%D9%83%D9%88%D9%86%D8%BA%D9%88-%D8%A7%D9%84%D8%AF%D9%8A%D9%85%D9%82%D8%B1%D8%A7%D8%B7%D9%8A%D8%A9/",
    "https://edaegypt.gov.eg/ar/%D8%B9%D9%86-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D8%AA%D8%A3%D8%B3%D9%8A%D8%B3-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/",
    
    
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
        response = st.session_state.chat.send_message(text_content)

        # Append model's response to chat session
        st.session_state.chat_session.append({'user': {'role': 'model', 'parts': [response.text]}})

# Display chat history
for message in st.session_state.chat_session:
    role, parts = message['user']['role'], message['user']['parts']
    with st.expander(f"{role.capitalize()} says:"):
        st.write(parts[0])  # Assuming only text for simplicity
