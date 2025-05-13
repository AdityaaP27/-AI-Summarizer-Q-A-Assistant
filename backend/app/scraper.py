# backend/app/scraper.py

import requests
from bs4 import BeautifulSoup

def fetch_and_clean_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "footer", "header", "nav"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text
