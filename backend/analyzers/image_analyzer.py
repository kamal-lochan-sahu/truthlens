import requests
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from io import BytesIO

print("Loading Vision Model (CLIP)... This might take a minute to download.")
model_id = "openai/clip-vit-base-patch32"
# CLIP model aur processor load karna
model = CLIPModel.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

def analyze_image_context(image_url: str, headline: str):
    """
    Checks if the given image actually matches the news headline.
    Returns a similarity score.
    """
    try:
        if not image_url:
            return {"success": False, "error": "No image URL provided"}

        # 1. Internet se image download karna
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")

        # 2. Options set karna (True headline vs False situations)
        # Model in teeno mein se sabse best match dhundhega
        choices = [
            headline, 
            "A generic unrelated background image", 
            "A completely random picture"
        ]
        
        # 3. Model ko data pass karna
        inputs = processor(text=choices, images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        
        # 4. Score calculate karna
        logits_per_image = outputs.logits_per_image 
        probs = logits_per_image.softmax(dim=1).detach().numpy()[0]

        # Humare main headline ka probability score (0 to 100)
        match_score = round(float(probs[0]) * 100, 2)

        return {
            "success": True,
            "headline_match_score": match_score,
            "is_suspicious": match_score < 20.0, # Agar match 20% se kam hai, matlab jhol hai
            "message": "Image matches context" if match_score >= 20.0 else "Image context mismatch detected!"
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# Local test ke liye
if __name__ == "__main__":
    # Test ke liye hum ek Cute Dog ki free photo le rahe hain
    test_image_url = "https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8"
    
    # Test 1: Sahi Context (Dog ki photo ke saath Dog ki baat)
    true_headline = "A cute dog looking at the camera"
    print(f"\n--- Test 1 (Real Context) ---")
    print(f"Headline: '{true_headline}'")
    print("Result:", analyze_image_context(test_image_url, true_headline))
    
    # Test 2: Galat Context (Dog ki photo par Riot ki headline)
    fake_headline = "Dangerous riots erupt in Paris streets"
    print(f"\n--- Test 2 (Fake Context) ---")
    print(f"Headline: '{fake_headline}'")
    print("Result:", analyze_image_context(test_image_url, fake_headline))