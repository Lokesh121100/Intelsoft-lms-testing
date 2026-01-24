
import requests
from bs4 import BeautifulSoup
import re

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
    
    # Login
    print("=== Authenticating ===")
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'logintoken'})
    if not token_input: raise Exception("No login token")
    
    payload = {'username': USERNAME, 'password': PASSWORD, 'logintoken': token_input['value']}
    post_response = session.post(LOGIN_URL, data=payload)
    if "Dashboard" not in post_response.text: raise Exception("Login failed")
    print("[OK] Login Successful")
    return session

def verify_user_profile(session):
    print("\n=== 1. Checking User Profile (op_user) ===")
    # First search for the user to get their ID (or just iterate known IDs if we knew them)
    # We'll use the user browser page to find a link
    users_url = f"{BASE_URL}/admin/user.php"
    resp = session.get(users_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Look for any user link that isn't the admin
    user_links = soup.select('a[href*="/user/profile.php"]')
    target_link = None
    
    for link in user_links:
        if "id=" in link['href']:
            # grab the first one that looks like a normal user profile
            target_link = link['href']
            print(f"  [INFO] Found profile link: {link.get_text()} -> {target_link}")
            if "admin" not in link.get_text().lower(): # Prefer non-admin if possible
                break
    
    if target_link:
        resp = session.get(target_link)
        if "Edit profile" in resp.text:
             print(f"  [OK] Verified 'Edit profile' link exists for user.")
        else:
             print(f"  [X] 'Edit profile' link MISSING.")
    else:
        print("  [?] Could not find any user links to test.")

def verify_course_actions(session):
    print("\n=== 2. Checking Course Edit/Delete Capability ===")
    # Go to Manage Courses
    manage_url = f"{BASE_URL}/course/management.php"
    resp = session.get(manage_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # We look for "AWS Check Course" which we created
    course_text = soup.find(string=re.compile("AWS Check Course"))
    
    if course_text:
        print("  [OK] Found 'AWS Check Course' in management list.")
        # Attempt to find the parent container to get action links
        # This is tricky with BS4 on complex Moodle tables, simplified check:
        if "action=edit" in resp.text:
             print("  [OK] Found 'Edit' action links in the page.")
        if "action=delete" in resp.text:
             print("  [OK] Found 'Delete' action links in the page.")
    else:
        print("  [!] 'AWS Check Course' not found. Searching for any course...")
        if "action=edit" in resp.text:
             print("  [OK] Found 'Edit' action links (General check).")
        else:
             print("  [X] No 'Edit' links found on Management page.")

if __name__ == "__main__":
    try:
        s = get_authenticated_session()
        verify_user_profile(s)
        verify_course_actions(s)
    except Exception as e:
        print(f"FATAL: {e}")
