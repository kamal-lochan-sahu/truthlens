from transformers import pipeline

print("Loading AI Model (This might take a minute to download on first run)...")
# Pipeline automatically model ko download aur load kar legi
fake_news_analyzer = pipeline("text-classification", model="roberta-base-openai-detector")

def analyze_text(text: str):
    """
    Analyzes text using HuggingFace RoBERTa model.
    Returns Real/Fake classification and confidence score.
    """
    try:
        if not text or len(text.strip()) == 0:
            return {"success": False, "error": "No text provided"}

        # AI Models ki ek token limit hoti hai (usually 512 tokens).
        # Isliye hum safe rehne ke liye first 400 words ko hi analyze karenge.
        words = text.split()
        safe_text = " ".join(words[:400])

        # Run ML model
        result = fake_news_analyzer(safe_text)
        
        # Result extract karna (HuggingFace returns a list like: [{'label': 'Fake', 'score': 0.95}])
        label = result[0]['label']
        score = result[0]['score']

        return {
            "success": True,
            "label": label,  # 'Fake' or 'Real'
            "confidence": round(score * 100, 2), # Convert 0.95 to 95.00%
            "analyzed_words": len(words[:400])
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# Local test ke liye (Ek ekdum fake sounding text daala hai)
if __name__ == "__main__":
    sample_fake_text = "Scientists have discovered that eating 10 kgs of chocolate every day makes you immortal. The government is hiding this secret to control the population. Share this immediately!"
    print("\nAnalyzing sample text...")
    result = analyze_text(sample_fake_text)
    print("AI Verdict:", result)