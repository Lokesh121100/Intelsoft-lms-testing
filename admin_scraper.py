
import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://lms-demo.intelsoft.sg"
LOGIN_URL = f"{BASE_URL}/login/index.php"
OUTPUT_DIR = "scraped_pages"

# Define the pages we want to scrape to understand the admin features
TARGET_PAGES = {
    "dashboard": f"{BASE_URL}/my/",
    "site_admin": f"{BASE_URL}/admin/search.php",
    "user_management": f"{BASE_URL}/admin/user.php",
    "course_management": f"{BASE_URL}/course/management.php",
    "plugins_overview": f"{BASE_URL}/admin/plugins.php",
    "notifications": f"{BASE_URL}/message/output/popup/notifications.php",
}

USERNAME = "admin"
PASSWORD = "Password@123"

def login_and_scrape():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    print("1. Logging in...")
    try:
        # Get Token
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'logintoken'})
        
        if not token_input:
            print("Failed to find login token.")
            return

        login_token = token_input['value']
        
        # Post Credentials
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'logintoken': login_token,
            'anchor': ''
        }
        
        post_response = session.post(LOGIN_URL, data=payload)
        
        if "Dashboard" not in post_response.text and "my/index.php" not in post_response.url:
            print("Login failed.")
            return

        print("Login Successful. Starting Scraping...")

        # Scrape Targets
        for name, url in TARGET_PAGES.items():
            print(f"Scraping {name} ({url})...")
            page_response = session.get(url)
            
            if page_response.status_code == 200:
                filename = os.path.join(OUTPUT_DIR, f"{name}.html")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(page_response.text)
                print(f"Saved to {filename}")
            else:
                print(f"Failed to fetch {name}. Status: {page_response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    login_and_scrape()
