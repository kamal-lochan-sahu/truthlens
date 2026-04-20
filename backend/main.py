from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Saare custom AI aur Scraper tools import kar rahe hain
from scrapers.article_scraper import scrape_article
from analyzers.text_analyzer import analyze_text
from analyzers.fact_checker import check_facts
from analyzers.image_analyzer import analyze_image_context
from analyzers.vision_engine import extract_text_with_gemini

app = FastAPI(title="TruthLens Core API v2.0")

# CORS Setup: Taki Next.js frontend isse block na kare
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# V1 ke liye Input Schema
class ArticleRequest(BaseModel):
    url: str
    image_url: str | None = None 

@app.get("/")
def home():
    return {"message": "TruthLens Backend v2.0 is Running smoothly! 🚀"}

# ==========================================
# VERSION 1: LINK / URL ANALYZER ENDPOINT
# ==========================================
@app.post("/api/analyze")
async def analyze_article(req: ArticleRequest):
    print(f"\n--- New URL Request Received for: {req.url} ---")
    
    # 1. Scrape the article
    print("1. Scraping article...")
    scrape_res = scrape_article(req.url)
    if not scrape_res.get("success"):
        raise HTTPException(status_code=400, detail="Could not extract text from this URL")
    
    title = scrape_res["title"]
    text = scrape_res["text"]

    # 2. Text Pattern Analysis
    print("2. Analyzing Text Patterns...")
    text_analysis = analyze_text(text)

    # 3. Fact Checking API
    print("3. Checking Facts on Google...")
    fact_check = check_facts(title)

    # 4. Image Context Analysis (CLIP)
    image_analysis = None
    if req.image_url:
        print("4. Analyzing Image Context...")
        image_analysis = analyze_image_context(req.image_url, title)

    print("--- URL Analysis Complete ---")
    return {
        "success": True,
        "data": {
            "title": title,
            "text_analysis": text_analysis,
            "fact_check": fact_check,
            "image_analysis": image_analysis
        }
    }

# ==========================================
# VERSION 2: GEMINI VISION / IMAGE UPLOAD ENDPOINT
# ==========================================
@app.post("/api/analyze-upload")
async def analyze_uploaded_image(file: UploadFile = File(...)):
    print(f"\n--- New Image Uploaded: {file.filename} ---")
    
    try:
        image_bytes = await file.read()
        
        # 1. Gemini AI se Text Extract karna
        print("1. Extracting text using Gemini Vision AI...")
        extracted_text = extract_text_with_gemini(image_bytes)
        
        if not extracted_text:
            return {"success": False, "error": "Could not read any text from the image."}
            
        print(f"-> Text Extracted! ({len(extracted_text)} characters)")
        
        # 2. Jo text nikala, usko apne AI Analyzer se check karwana (AI vs Human)
        print("2. Analyzing Text Patterns...")
        text_analysis = analyze_text(extracted_text)

        # 3. Google API par Fact Check karna (Start ka thoda hissa as a claim use karke)
        print("3. Checking Facts on Google...")
        fact_check = check_facts(extracted_text[:200]) 

        print("--- Image Analysis Complete ---")
        return {
            "success": True,
            "data": {
                "title": "Image Screenshot Analysis",
                "extracted_text": extracted_text, # Dikhane ke liye ki AI ne kya padha
                "text_analysis": text_analysis,
                "fact_check": fact_check
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Server Run Command
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)