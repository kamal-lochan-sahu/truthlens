---
title: TruthLens API
emoji: 👁️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
short_description: AI-powered Misinformation & Fake News Detector API.
---

# 👁️ TruthLens API v2.0 - Deep Fake & Misinformation Detector

Welcome to the backend engine of **TruthLens**, a robust AI-powered API designed to combat the spread of fake news, manipulated screenshots, and misinformation on the internet.

### 🚀 What does it do?
This API serves as a dual-mode fact-checking engine:
1. **URL Scanner:** Scrapes news articles from given web links, extracts the core text, and runs NLP analysis to detect misleading patterns.
2. **Image/Screenshot Scanner:** Bypasses traditional text limitations by utilizing **Google's Gemini 2.5 Flash Vision AI** to extract text directly from WhatsApp forwards, social media screenshots, or images, and cross-references the claims with official fact-checking databases.

### 🛠️ Tech Stack & Architecture
* **Framework:** FastAPI (Python)
* **Vision & OCR:** Google Gemini 2.5 Flash
* **Verification:** Google Fact-Check Tools API
* **Scraping:** Newspaper3k & BeautifulSoup4
* **Deployment:** Hugging Face Spaces (Dockerized, 16GB RAM)

### 👨‍💻 Developer
Developed by **Kamal Lochan Sahu** - Full-Stack & ML Engineer.