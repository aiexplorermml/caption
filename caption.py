import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# Load API key from environment variable or Streamlit secrets
API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit app title
st.title("📷 Photo Caption Generator")

# File uploader for images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate caption for the image
    if st.button("Generate Caption"):
        try:
            # Convert image to bytes
            image_bytes = uploaded_file.getvalue()

            # Use Gemini to generate a caption
            response = model.generate_content(
                contents=[
                    "Generate a creative and descriptive caption for this image:",
                    image_bytes
                ]
            )

            # Display the generated caption
            st.subheader("Generated Caption:")
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
