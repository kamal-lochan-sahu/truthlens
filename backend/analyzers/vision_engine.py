import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# 🔒 SECURITY FIX: API Key ab code mein nahi hai. Yeh direct Hugging Face se aayegi.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini with the safe key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_text_with_gemini(image_bytes: bytes) -> str:
    """
    Sends the image to Google's Gemini model to extract text with high accuracy.
    """
    try:
        # Key missing check
        if not GEMINI_API_KEY:
            return "Error: API Key missing in server settings."

        image = Image.open(BytesIO(image_bytes))
        
        # Using the stable 1.5 Flash version
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        prompt = "Extract all the readable text from this image accurately. Do not add any extra comments or markdown, just return the raw text."
        
        response = model.generate_content([prompt, image])
        
        if response and response.text:
            return response.text.strip()
        return ""
        
    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        return ""