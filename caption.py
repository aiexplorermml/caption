import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Load API key
API_KEY = "AIzaSyBsq5Kd5nJgx2fejR77NT8v5Lk3PK4gbH8"

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit app title
st.title("📷 Photo Caption Generator")

# Warning message
st.warning("⚠️ Please wait 30 seconds between requests to avoid rate limits")

@st.cache_data(show_spinner=False)
def generate_caption(image_bytes, mime_type):
    """Generate caption with caching to avoid repeated API calls"""
    time.sleep(1)  # Add delay to prevent rate limiting
    response = model.generate_content(
        contents=[
            "Generate a creative and descriptive caption for this image:",
            {"mime_type": mime_type, "data": image_bytes}
        ]
    )
    return response.text

# File uploader for images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate caption for the image
    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating caption..."):
                # Convert image to bytes
                image_bytes = uploaded_file.getvalue()
                
                # Generate caption using cached function
                caption = generate_caption(image_bytes, uploaded_file.type)

            # Display the generated caption
            st.subheader("Generated Caption:")
            st.success(caption)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("""
            ⚠️ Rate limit exceeded. Please:
            - Wait 1-2 minutes before trying again
            - Don't click the button multiple times quickly
            """)
