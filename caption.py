import streamlit as st
from PIL import Image
import requests
import configparser

# Load token from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['DEFAULT']['HF_API_TOKEN']

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

def generate_caption(image_bytes):
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        elif response.status_code == 503:
            return "🔄 Model is loading... Please wait 10 seconds and try again."
        else:
            return "❌ API Error. Please check your token and try again."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title("📷 FREE Photo Caption Generator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("🎯 Generate Caption"):
        with st.spinner("AI is analyzing your image..."):
            image_bytes = uploaded_file.getvalue()
            caption = generate_caption(image_bytes)
            st.subheader("📝 Generated Caption:")
            st.success(caption)
