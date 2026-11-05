import os
import requests
from bs4 import BeautifulSoup

def fetch_page_data(url):
    """
    Fetches the HTML content of a URL with safety headers to mimic a real browser.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"\n[INFO] Connecting to {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes (404, 500, etc.)
        response.raise_for_status()
        return response.text
        
    except requests.exceptions.HTTPError as http_err:
        print(f"[ERROR] HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("[ERROR] The request timed out. Try again later.")
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] An error occurred: {err}")
    return None

def parse_html(html_content):
    """
    Parses HTML content to extract the Title, Headings, and Links.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract metadata
    page_title = soup.title.string.strip() if soup.title else "No Title Found"
    
    # Extract structural headings
    headings = []
    for tag in ['h1', 'h2', 'h3']:
        for heading in soup.find_all(tag):
            text = heading.get_text().strip()
            if text:
                headings.append(f"[{tag.upper()}] {text}")
                
    # Extract hyperlinks
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text().strip() or "Link"
        if href.startswith('http'): # Focus on external/absolute links
            links.append(f"{text}: {href}")
            
    return page_title, headings, links

def save_to_file(title, headings, links, filename="scraped_data.txt"):
    """
    Saves parsed data cleanly into a local text file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"SCRAPED DATA FOR: {title}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"--- HEADINGS ({len(headings)}) ---\n")
            for h in headings:
                f.write(f"{h}\n")
                
            f.write(f"\n--- LINKS ({len(links)}) ---\n")
            for l in links[:50]: # Cap at 50 links for neatness
                f.write(f"{l}\n")
                
        print(f"[SUCCESS] Data safely exported to '{filename}'")
    except IOError as e:
        print(f"[ERROR] Failed to save data to file: {e}")

def main():
    print("=== Welcome to the Simple Web Scraper ===")
    target_url = input("Enter a public URL to scrape (e.g., https://example.com): ").strip()
    
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    html = fetch_page_data(target_url)
    
    if html:
        title, headings, links = parse_html(html)
        print(f"\n[SUCCESS] Successfully parsed page: '{title}'")
        print(f"Found {len(headings)} headings and {len(links)} links.")
        
        save_to_file(title, headings, links)
    else:
        print("[FAILED] Could not retrieve or parse the target webpage.")

if __name__ == "__main__":
    main()
