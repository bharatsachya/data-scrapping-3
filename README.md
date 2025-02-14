# Smashing Magazine Article Scraper

This project is a web scraper that collects articles from [Smashing Magazine](https://www.smashingmagazine.com/articles/) and saves the data to a JSON file. The scraper extracts the following details for each article:

- **URL**: The link to the article.
- **Title**: The title of the article.
- **Author**: The author of the article.
- **Date**: The publication date of the article.
- **Categories**: The categories/tags associated with the article.
- **Summary**: A quick summary of the article.
- **Content**: The main content of the article.

The scraper uses **parallelism** to speed up the process by dividing the work among multiple threads.

---

## Features

- **Pagination Handling**: Scrapes articles from multiple pages.
- **Parallel Scraping**: Uses `ThreadPoolExecutor` to scrape articles concurrently.
- **Error Handling**: Gracefully handles errors and skips problematic articles.
- **JSON Output**: Saves the scraped data to a JSON file (`smashingMagazineArticles.json`).

---

## Requirements

- Python 3.7+
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `concurrent.futures`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smashing-magazine-scraper.git
   cd smashing-magazine-scraper
