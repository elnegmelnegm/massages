import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import genai  # Assuming you have the genai library installed

# Function to load the generative model
@st.cache_resource
def load_model() -> genai.GenerativeModel:
    model = genai.GenerativeModel('gemini-pro')
    return model

# Function to scrape data from the given URL
def scrape_eda_data():
    url = "https://edaegypt.gov.eg/ar/%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D9%8A%D8%A6%D8%A9/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA/%D9%85%D9%86%D8%B4%D9%88%D8%B1%D8%A7%D8%AA-%D8%AF%D9%88%D8%B1%D9%8A%D8%A9/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant data using BeautifulSoup
    # Your scraping logic here
    # For example, let's assume the data is in a div with class "publication"
    publications = soup.find_all('div', class_='publication')

    return publications

# Streamlit app
st.set_page_config(
    page_title="EDA Healthcare Chat",
    layout="wide",
)

st.title("EDA Healthcare Chat")

# Load the generative model
model = load_model()

# Scrape data from the website
scraped_data = scrape_eda_data()

# Display scraped data (for demonstration purposes)
st.subheader("Latest Publications:")
for publication in scraped_data:
    st.write(publication.text)

# Patient interaction section
st.header("Ask a Health Question")

# Allow the patient to ask a question
patient_question = st.text_input("Ask your health-related question:")

# If the patient has asked a question, generate a response
if patient_question:
    # Use the scraped data or any other logic to generate a response
    # For now, let's just echo the question as a response
    st.text(f"You asked: {patient_question}")

    # Generate a response using the loaded generative model
    response = model.generate_content(patient_question)
    response.resolve()

    # Display the generated response
    st.text("AI Response:")
    st.write(response.text)

# Note: Add more features and logic to enhance the app as needed
