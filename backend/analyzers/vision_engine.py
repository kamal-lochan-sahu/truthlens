import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Yahan apni real Gemini API Key daalni hai (Jo tumne Google AI Studio se li hogi)
# (Agar abhi nahi hai, toh aistudio.google.com se free mein 1 minute mein ban jayegi)
GEMINI_API_KEY = "AIzaSyDoIBJbtUzPfJFnDGQ560dl60bgtTQcR9Q" 

genai.configure(api_key=GEMINI_API_KEY)

def extract_text_with_gemini(image_bytes: bytes) -> str:
    """
    Sends the image to Google's Gemini 1.5 Flash model to extract text with high accuracy.
    """
    try:
        # Convert raw bytes to Pillow Image
        image = Image.open(BytesIO(image_bytes))
        
        # Load the fastest multimodal model
        model = genai.GenerativeModel('gemini-2.5-flash')  # Upgrade to Version 2.5!
        
        # Hamari strict instruction
        prompt = "Extract all the readable text from this image accurately. Do not add any extra comments or markdown, just return the raw text."
        
        # AI se response lena
        response = model.generate_content([prompt, image])
        
        return response.text.strip()
    
    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        return ""