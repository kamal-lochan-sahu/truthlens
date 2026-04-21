import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# 🔒 Direct Hugging Face Settings se key aayegi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_text_with_gemini(image_bytes: bytes) -> str:
    try:
        if not GEMINI_API_KEY:
            return "Error: API Key missing in server settings."

        image = Image.open(BytesIO(image_bytes))
        
        # 🔥 TUMHARI DEMAND: Exactly 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        prompt = "Extract all the readable text from this image accurately. Do not add any extra comments or markdown, just return the raw text."
        response = model.generate_content([prompt, image])
        
        if response and response.text:
            return response.text.strip()
        return ""
        
    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        return ""