from newspaper import Article
import requests
from bs4 import BeautifulSoup

def scrape_article(url: str):
    """
    Given a news article URL, extracts the main title and body text.
    """
    try:
        # Newspaper3k se smartly scrape karne ki koshish
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            return {
                "success": True,
                "title": article.title,
                "text": article.text
            }
            
        # Fallback: Agar newspaper3k fail ho jaye, toh BeautifulSoup use karenge
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Paragraphs nikalna
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        return {
            "success": True,
            "title": soup.title.string if soup.title else "No Title",
            "text": text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Local test ke liye
if __name__ == "__main__":
    test_url = "https://www.bbc.com/news/world-us-canada-68000000"
    result = scrape_article(test_url)
    print("Scraping Test Result:", result)