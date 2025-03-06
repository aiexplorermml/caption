import openai
from PIL import Image
import requests
from io import BytesIO

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Function to generate a caption for an image
def generate_photo_caption(image_url):
    # Step 1: Analyze the image (you can use an image recognition API here if needed)
    # For simplicity, we'll assume the image is already described or use a placeholder.
    image_description = "A beautiful sunset over the mountains with a calm lake in the foreground."

    # Step 2: Use OpenAI GPT to generate a caption
    prompt = f"Generate a short and engaging caption for this photo: {image_description}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate GPT model
        prompt=prompt,
        max_tokens=50,  # Limit the caption length
        n=1,  # Number of captions to generate
        stop=None,  # No specific stop sequence
        temperature=0.7,  # Controls creativity (0 = strict, 1 = creative)
    )

    # Extract the generated caption
    caption = response.choices[0].text.strip()
    return caption

# Example image URL
image_url = "https://example.com/sunset.jpg"

# Generate and print the caption
caption = generate_photo_caption(image_url)
print("Generated Caption:", caption)
