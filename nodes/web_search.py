import os
import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, Any
from models import AgentState

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults

# Load environment variables from .env file
load_dotenv()

def scrape_daraz(keyword: str, limit: int = 12) -> Dict:
    """Improved Daraz scraper for Bangladesh"""
    print(f"🔍 Scraping Daraz for: {keyword}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
    }
    
    url = f"https://www.daraz.com.bd/catalog/?q={requests.utils.quote(keyword)}"
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        products = []
        
        # Try to extract JSON data from script tags
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and ("__INITIAL_STATE__" in script.string or "window.pageData" in script.string):
                try:
                    # Find JSON object
                    match = re.search(r'({.+?});', script.string, re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        
                        items = []
                        if isinstance(data, dict):
                            mods = data.get("mods", {}) or data.get("data", {}).get("mods", {})
                            items = mods.get("listItems", []) or []
                        
                        for item in items[:limit]:
                            products.append({
                                "name": item.get("name"),
                                "price": item.get("price"),
                                "original_price": item.get("originalPrice"),
                                "discount": item.get("discount"),
                                "rating": item.get("ratingScore"),
                                "sold": item.get("itemSold") or item.get("sold"),
                                "link": "https:" + item.get("productUrl", "") if item.get("productUrl") else None,
                            })
                        if products:
                            break
                except:
                    continue
        
        # Fallback scraping
        if len(products) < 3:
            cards = soup.select('div[data-qa-locator="product-item"]')[:limit]
            for card in cards:
                name = card.select_one('a.title, .product-title')
                price = card.select_one('span.currency, .price')
                products.append({
                    "name": name.get_text(strip=True) if name else None,
                    "price": price.get_text(strip=True) if price else None,
                })
        
        return {
            "keyword": keyword,
            "total_found": len(products),
            "products": products[:limit]
        }
        
    except Exception as e:
        print(f"Daraz scrape error: {e}")
        return {"error": str(e), "products": []}


def web_search_node(state: AgentState):
    query = state.get('query', '')
    print(f"🌍 Dynamic Web Search Triggered for: {query}")
    
    merged = state.get("merged_results", [])
    
    # === Tavily Search (High Quality) ===
    try:
        tavily = TavilySearchResults(
            max_results=8,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False
        )
        
        tavily_results = tavily.invoke(f"{query} daraz bd price OR trending OR bestseller OR best seller")
        merged.append({
            "source": "tavily_search",
            "content": tavily_results
        })
        print("✅ Tavily Search Successful")
    except Exception as e:
        print(f"Tavily failed: {e}")
    
    # === Daraz Direct Scrape ===
    try:
        daraz_data = scrape_daraz(query)
        merged.append({
            "source": "daraz_direct",
            "content": daraz_data
        })
        print("✅ Daraz Scrape Completed")
    except Exception as e:
        print(f"Daraz scrape failed: {e}")
    
    return {"merged_results": merged}