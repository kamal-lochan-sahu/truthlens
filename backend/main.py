from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Yeh hain asli imports jo missing the
from scrapers.article_scraper import scrape_article
from analyzers.text_analyzer import analyze_text
from analyzers.fact_checker import check_facts
from analyzers.image_analyzer import analyze_image_context

app = FastAPI(title="TruthLens Core API")

# CORS Setup: Frontend (Next.js) se connectivity ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend se kaisa data aayega uski definition
class ArticleRequest(BaseModel):
    url: str
    image_url: str | None = None 

@app.get("/")
def home():
    return {"message": "TruthLens Backend is Running smoothly! 🚀"}

@app.post("/api/analyze")
async def analyze_article(req: ArticleRequest):
    print(f"\n--- New Request Received for: {req.url} ---")
    
    # 1. Scrape the article
    print("1. Scraping article...")
    scrape_res = scrape_article(req.url)
    if not scrape_res.get("success"):
        raise HTTPException(status_code=400, detail="Could not extract text from this URL")
    
    title = scrape_res["title"]
    text = scrape_res["text"]

    # 2. Text Pattern Analysis (AI vs Human)
    print("2. Analyzing Text Patterns...")
    text_analysis = analyze_text(text)

    # 3. Fact Checking API (Google Fact Check)
    print("3. Checking Facts on Google...")
    fact_check = check_facts(title)

    # 4. Image Context Analysis (CLIP Model)
    image_analysis = None
    if req.image_url:
        print("4. Analyzing Image Context...")
        image_analysis = analyze_image_context(req.image_url, title)

    print("--- Analysis Complete ---")
    
    return {
        "success": True,
        "data": {
            "title": title,
            "text_analysis": text_analysis,
            "fact_check": fact_check,
            "image_analysis": image_analysis
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)