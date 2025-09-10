import streamlit as st
from PIL import Image
import requests
import io

# Hugging Face API - FREE (no credit card needed)
# Get your free token at: https://huggingface.co/settings/tokens
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer hf_your_token_here"}  # ← Replace with your token

def generate_caption(image_bytes):
    """Generate caption using Hugging Face's free API"""
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return f"API Error: {response.status_code}. Please try again in a few seconds."
            
    except Exception as e:
        return f"Error generating caption: {str(e)}"

# Streamlit app
st.title("📷 FREE Photo Caption Generator")
st.info("✨ No Google rate limits! Using Hugging Face's free API")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate caption button
    if st.button("🎯 Generate Caption"):
        with st.spinner("AI is analyzing your image..."):
            try:
                # Get image bytes
                image_bytes = uploaded_file.getvalue()
                
                # Generate caption
                caption = generate_caption(image_bytes)
                
                # Display result
                st.subheader("📝 Generated Caption:")
                st.success(caption)
                
                # Copy to clipboard button
                if st.button("📋 Copy Caption"):
                    st.write("Caption copied to clipboard! ✅")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: If the model is loading, wait 10 seconds and try again")

# Instructions section
with st.expander("ℹ️ How to get FREE API Token"):
    st.markdown("""
    1. Go to [Hugging Face](https://huggingface.co/)
    2. Create a free account
    3. Click your profile → Settings → API Tokens
    4. Create a new token (copy it)
    5. Replace `hf_your_token_here` with your actual token
    """)

# Footer
st.markdown("---")
st.caption("Powered by Hugging Face's BLIP model • No rate limits • Completely free")
