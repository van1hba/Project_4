# scanner/site_crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()  # store visited URLs to avoid duplicates and infinite loops

def get_links(start_url, max_pages=100):
    """
    Crawl the start_url and return a list of internal links found.
    - start_url: full URL to begin crawling from
    - max_pages: safety limit to avoid crawling too much
    """
    pages = []
    to_visit = [start_url]

    base_domain = urlparse(start_url).netloc

    while to_visit and len(pages) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            resp = requests.get(url, timeout=6)
            visited.add(url)
            pages.append(url)

            soup = BeautifulSoup(resp.text, "html.parser")

            # find all <a> tags
            for tag in soup.find_all("a"):
                link = tag.get("href")
                if not link:
                    continue

                # convert relative → absolute URL
                full_url = urljoin(url, link)

                # keep internal domain only
                if urlparse(full_url).netloc != base_domain:
                    continue

                # avoid unwanted schemes
                if not full_url.startswith("http"):
                    continue
                if full_url.startswith("mailto:"):
                    continue
                if "#" in full_url:
                    continue

                if full_url not in visited:
                    to_visit.append(full_url)

        except Exception as e:
            print(f"[crawl error] {url} -> {e}")

    return pages
