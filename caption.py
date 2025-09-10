import streamlit as st
from PIL import Image
import requests
import os

# Load token safely from secrets
API_TOKEN = st.secrets.get("HF_API_TOKEN", "")

headers = {"Authorization": f"Bearer {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}"}
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

if not API_TOKEN:
    st.error("❌ API token not configured. Please follow the instructions below.")
    st.info("""
    **How to set up:**
    1. Get free token from: https://huggingface.co/settings/tokens
    2. Create a file called `.streamlit/secrets.toml`
    3. Add this line: `HF_API_TOKEN = "your_token_here"`
    4. Restart the app
    """)
else:
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
