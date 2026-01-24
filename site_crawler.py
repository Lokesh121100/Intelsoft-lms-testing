import asyncio
import json
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urljoin

START_URL = "https://lms-demo.intelsoft.sg/"
MAX_PAGES = 50  # Limit to prevent infinite crawling
OUTPUT_FILE = "site_map.json"

visited_urls = set()
site_map = []

def is_internal_link(base, link):
    return urlparse(link).netloc == urlparse(base).netloc

async def crawl(page, url):
    if url in visited_urls or len(visited_urls) >= MAX_PAGES:
        return
    
    print(f"Crawling: {url}")
    visited_urls.add(url)
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        title = await page.title()
        
        # Add to map
        site_map.append({
            "url": url,
            "title": title,
            "status": "Accessible"
        })
        
        # Find all links
        links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a')).map(a => a.href)
        """)
        
        # Filter internal links
        internal_links = [l for l in links if is_internal_link(START_URL, l)]
        
        # Recursive crawl (Breadth-first approach would be better, but simple recursion for now)
        for link in set(internal_links):
            if link not in visited_urls and not link.endswith(('.pdf', '.jpg', '.png', '#')):
                await crawl(page, link)
                
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        site_map.append({
            "url": url,
            "error": str(e),
            "status": "Error"
        })

START_URL = "https://lms-demo.intelsoft.sg/admin/search.php" # Start in Site Admin
LOGIN_URL = "https://lms-demo.intelsoft.sg/login/index.php"
USERNAME = "admin"
PASSWORD = "Password@123"

async def login(page):
    print(f"Logging in as {USERNAME}...")
    await page.goto(LOGIN_URL, wait_until="domcontentloaded")
    await page.fill("input[name='username']", USERNAME)
    await page.fill("input[name='password']", PASSWORD)
    await page.click("#loginbtn")
    await page.wait_for_load_state("domcontentloaded")
    
    # Verify login success
    if await page.query_selector(".logininfo a[href*='logout']"):
        print("Login Successful!")
    else:
        print("Login Failed! Check credentials.")
        # Proceeding anyway to see what happens, or could return False
        
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Visual debugging
        context = await browser.new_context()
        page = await context.new_page()
        
        await login(page)
        
        # Start crawl at Admin Search to map features
        await crawl(page, START_URL)
        
        await browser.close()
        
    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(site_map, f, indent=2)
    
    print(f"Crawl complete. Mapped {len(site_map)} pages. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
