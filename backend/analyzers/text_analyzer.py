import os
import json
import google.generativeai as genai

# Wahi tijori wali key jo humne pehle set ki thi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_text(text: str) -> dict:
    """
    Analyzes text using Gemini to determine if it's Real or Fake.
    Returns dict: {"success": True/False, "label": "Real" | "Fake", "confidence": int}
    """
    try:
        if not text or len(text.strip()) == 0:
            return {"success": False, "error": "No text provided", "label": "UNKNOWN", "confidence": 0}

        if not GEMINI_API_KEY:
            print("Warning: API Key missing!")
            return {"success": False, "error": "API Key missing", "label": "UNKNOWN", "confidence": 0}

        # Safe limit
        safe_text = text[:5000]

        # Wahi naya model jo tumne demand kiya tha
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 🧠 The Magic Prompt: AI ko strictly JSON format mein answer dene bolenge
        prompt = f"""
        You are an expert AI fact-checker and misinformation detector. 
        Read the following text (which might be extracted from a newspaper or social media) and determine if it looks like authentic news/information ("Real") or fabricated/fake news ("Fake").
        
        Return ONLY a valid JSON object exactly like this format without any extra markdown or text:
        {{"label": "Real", "confidence": 95}}
        or
        {{"label": "Fake", "confidence": 88}}
        
        Text to analyze:
        {safe_text}
        """
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            # Clean up formatting to safely extract JSON
            clean_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            try:
                data = json.loads(clean_text)
                
                label = str(data.get("label", "UNKNOWN")).capitalize()
                if label not in ["Real", "Fake"]:
                    label = "UNKNOWN"
                    
                confidence = int(data.get("confidence", 0))
                
                return {
                    "success": True,
                    "label": label,
                    "confidence": confidence
                }
            except json.JSONDecodeError:
                print(f"JSON Parse Error. Raw output: {clean_text}")
                return {"success": False, "error": "Failed to parse JSON", "label": "UNKNOWN", "confidence": 0}

    except Exception as e:
        print(f"Text Analysis Error: {e}")
        return {"success": False, "error": str(e), "label": "UNKNOWN", "confidence": 0}

    return {"success": False, "error": "Unknown error", "label": "UNKNOWN", "confidence": 0}
