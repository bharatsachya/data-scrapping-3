import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.smashingmagazine.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_article_links(page_url):
    """Get all article links from a listing page"""
    links = []

    print(f"Fetching URL: {page_url}")  # Debugging statement

    response = requests.get(page_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {page_url} - Status Code: {response.status_code}")
        return links

    soup = BeautifulSoup(response.text, 'html.parser')

    for article in soup.select("article.article--post"):
        a_tag = article.select_one("h2 a")
        if a_tag and a_tag.get("href"):
            links.append(a_tag["href"])

    return links

def get_article_details(article_url):
    """Get full details for a single article"""
    try:
        valid_url = f"{BASE_URL}{article_url}"
        response = requests.get(valid_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract basic info
        title = soup.select_one("article .article-header--title").text
        author = soup.select_one("article a").text
        # Date handling
        date_str = soup.select_one("article time").text

        # Categories
        categories = [(a.text.strip()) for a in soup.select(".subnav a")]
        # Summary and content
        summary = soup.select_one("article .article__summary").text
        paragraphs = [p.text.strip() for p in soup.select("div.c-garfield-summary ~ p")]
        # Combine everything into one text
        content = "\n".join(paragraphs)

        return {
            "url": article_url,
            "title": title,
            "author": author,
            "date": date_str,
            "categories": categories,
            "summary": summary,
            "content": content
        }

    except Exception as e:
        print(f"Error scraping {article_url}: {str(e)}")
        return None

def scrape_all_articles():
    """Main scraping function with pagination"""
    all_articles = []
    first_page_links = get_article_links(f"{BASE_URL}/articles")
    all_articles.extend([{"url": url} for url in first_page_links])
    page = 2
    
    # Phase 1: Collect all URLs
    while page< 10:  # Limit to 2 pages for testing
        page_url = f"{BASE_URL}/articles/page/{page}/"
        print(f"Scraping page {page} for links...")
        
        links = get_article_links(page_url)
        if not links:
            break
            
        # Create basic records without summary/content
        all_articles.extend([{"url": url} for url in links])
        page += 1
        time.sleep(1)  # Be polite

    return all_articles

def scrape_articles_parallel(article_list, num_workers=5):
    """Scrape articles in parallel using ThreadPoolExecutor"""
    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit tasks to the executor
        future_to_article = {
            executor.submit(get_article_details, article["url"]): article
            for article in article_list
        }
        
        # Process completed tasks
        for future in as_completed(future_to_article):
            article = future_to_article[future]
            try:
                data = future.result()
                if data:  # Only append if data is not None
                    results.append(data)
                    print(f"Scraped: {data['url']}")
            except Exception as e:
                print(f"Error scraping {article['url']}: {str(e)}")
    
    return results

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Step 1: Collect all article links
    print("Collecting article links...")
    articles = scrape_all_articles()
    print(f"Collected {len(articles)} articles.")
    
    # Step 2: Scrape articles in parallel
    print("Scraping articles in parallel...")
    scraped_data = scrape_articles_parallel(articles, num_workers=10)  # Use 10 workers
    
    # Step 3: Save data to JSON
    save_to_json(scraped_data, "smashingMagazineArticles.json")
    print("Scraping completed. Data saved to smashingMagazineArticles.json.")