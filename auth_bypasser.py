
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://lms-demo.intelsoft.sg/login/index.php"
DASHBOARD_URL = "https://lms-demo.intelsoft.sg/my/"
USERNAME = "admin"
PASSWORD = "Password@123"

def attempt_login():
    session = requests.Session()
    # Emulate a standard browser header to avoid immediate rejection
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    print("1. Fetching Login Page...")
    try:
        response = session.get(LOGIN_URL)
        if response.status_code != 200:
            print(f"Failed to fetch login page. Status: {response.status_code}")
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'logintoken'})
        
        if not token_input:
            print("Could not find 'logintoken'. WAF might be serving a challenge page.")
            return False
            
        login_token = token_input['value']
        print(f"Token found: {login_token}")
        
        print("2. Posting Credentials...")
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'logintoken': login_token,
            'anchor': ''
        }
        
        post_response = session.post(LOGIN_URL, data=payload)
        
        # Check if we are redirected to dashboard or still on login
        if "Dashboard" in post_response.text or "my/index.php" in post_response.url:
            print("LOGIN SUCCESS!")
            print(f"Current URL: {post_response.url}")
            return True
        elif "Invalid login" in post_response.text:
            print("Login Failed: Invalid Credentials.")
        else:
            print("Login Failed: Unknown Reason (Likely blocked or CAPTCHA).")
            # Save output for debug
            with open("login_fail.html", "w", encoding="utf-8") as f:
                f.write(post_response.text)
                
    except Exception as e:
        print(f"Error: {e}")
        
    return False

if __name__ == "__main__":
    attempt_login()
