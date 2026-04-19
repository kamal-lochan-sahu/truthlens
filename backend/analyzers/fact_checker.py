import os
import requests
from dotenv import load_dotenv

# .env file load karna
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

def check_facts(query: str):
    """
    Calls Google Fact Check Tools API to cross-reference claims.
    """
    if not GOOGLE_API_KEY:
        return {"success": False, "error": "Google API key is missing from .env"}

    # Query ko thoda chota karna taaki Google API ache se search kar sake
    search_query = " ".join(query.split()[:30]) 
    
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={search_query}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        # Agar claims mile
        if "claims" in data and len(data["claims"]) > 0:
            top_claim = data["claims"][0]
            claim_text = top_claim.get("text", "Unknown claim")
            
            # Review array se verdict nikalna
            reviews = top_claim.get("claimReview", [])
            if reviews:
                reviewer = reviews[0].get("publisher", {}).get("name", "Unknown Publisher")
                verdict = reviews[0].get("textualRating", "No rating")
                
                return {
                    "success": True,
                    "fact_found": True,
                    "claim": claim_text,
                    "reviewer": reviewer,
                    "verdict": verdict
                }

        # Agar koi claim na mile
        return {
            "success": True,
            "fact_found": False,
            "message": "No specific fact-checks found for this text."
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# Local test ke liye
if __name__ == "__main__":
    print("Testing Google Fact Check API...")
    # Ek famous fake claim
    test_claim = "The earth is flat and surrounded by an ice wall."
    result = check_facts(test_claim)
    print("Fact Check Result:", result)