
import requests
from bs4 import BeautifulSoup
import time

# Configuration
BASE_URL = "https://lms-demo.intelsoft.sg"
LOGIN_URL = f"{BASE_URL}/login/index.php"
USERNAME = "admin"
PASSWORD = "Password@123"

def get_authenticated_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    print("=== Authenticating ===")
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'logintoken'})
    
    if not token_input:
        raise Exception("Could not find login token.")

    login_token = token_input['value']
    
    payload = {
        'username': USERNAME,
        'password': PASSWORD,
        'logintoken': login_token,
        'anchor': ''
    }
    
    post_response = session.post(LOGIN_URL, data=payload)
    
    if "Dashboard" not in post_response.text and "my/index.php" not in post_response.url:
        raise Exception("Login failed.")
    
    print("[OK] Login Successful")
    return session

def verify_navigation_and_footer():
    try:
        session = get_authenticated_session()
        
        # Test Dashboard for Navigation and Footer
        dashboard_url = f"{BASE_URL}/my/"
        print(f"\n=== Verifying Dashboard Content ({dashboard_url}) ===")
        resp = session.get(dashboard_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text_content = soup.get_text()
        
        # Check Top Navigation Links
        nav_links = [
            "Home", 
            "Dashboard", 
            "My courses", 
            "Site administration"
            # "IOMAD dashboard" might be in a different menu or named differently, checking broadly
        ]
        
        print("Checking Navigation Links:")
        for link_text in nav_links:
            # We look for the text in the response (simple check)
            # A more robust check would verify <a> tags, but text presence is a good start
            if link_text in resp.text:
                print(f"  [OK] Found '{link_text}'")
            else:
                print(f"  [X] MISSING '{link_text}'")

        # Specific check for IOMAD dashboard (sometimes it's an icon or separate block)
        if "IOMAD dashboard" in resp.text or "Iomad dashboard" in resp.text:
             print(f"  [OK] Found 'IOMAD dashboard'")
        else:
             print(f"  [X] MISSING 'IOMAD dashboard'")

        # Check Footer
        print("Checking Footer:")
        if "Powered by Moodle" in resp.text:
            print("  [OK] Found 'Powered by Moodle'")
        else:
            print("  [X] MISSING 'Powered by Moodle'")
            
        if "Lorem Ipsum" not in resp.text:
            print("  [OK] Verified 'Lorem Ipsum' is NOT present")
        else:
            print("  [X] FAILED: Found 'Lorem Ipsum' placeholder text")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

def verify_iomad_packages():
    try:
        session = get_authenticated_session()
        dashboard_url = f"{BASE_URL}/blocks/iomad_company_admin/index.php"
        print(f"\n=== Verifying IOMAD Packages ({dashboard_url}) ===")
        
        resp = session.get(dashboard_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for "Package" related links
        links = soup.find_all('a')
        package_links = [l for l in links if 'package' in l.get_text().lower() or 'license' in l.get_text().lower()]
        
        if package_links:
            print(f"[OK] Found {len(package_links)} Package/License related links:")
            for l in package_links:
                print(f"  - {l.get_text().strip()} -> {l.get('href')}")
        else:
            print("[?] 'Packages' link not found explicitly on Dashboard. Checking for 'Manage' menu...")
            # Sometimes it's under a "Courses" or "Manage" dropdown
            manage_text = soup.find_all(string=lambda text: "manage" in text.lower() if text else False)
            if manage_text:
                 print(f"  [INFO] Found 'Manage' text phrases: {len(manage_text)}")
            else:
                 print("  [X] Could not find 'Packages' or 'Manage' links.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    verify_navigation_and_footer()
    verify_iomad_packages()
