
import requests
from bs4 import BeautifulSoup
import re

# Configuration
BASE_URL = "https://lms-demo.intelsoft.sg"
LOGIN_URL = f"{BASE_URL}/login/index.php"
# Student Credentials from checklist
USERNAME = "demolearner@moe.gov.sg"
PASSWORD = "Password@123"

def get_authenticated_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    print(f"=== Authenticating as Student ({USERNAME}) ===")
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
        print("[X] Login FAILED. Check credentials.")
        return None
    
    print("[OK] Login Successful")
    return session

def verify_student_dashboard(session):
    if not session: return
    
    print("\n=== 1. Verifying Dashboard & Enrollments ===")
    dashboard_url = f"{BASE_URL}/my/"
    resp = session.get(dashboard_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check for "My courses" check
    if "My courses" in resp.text:
        print("  [OK] Dashboard loaded with 'My courses' section.")
    else:
        print("  [?] 'My courses' text not explicitly found (might be named differently).")

    # Look for course cards
    # Just looking for links with /course/view.php?id= that are NOT the frontpage (id=1)
    course_links = soup.find_all('a', href=re.compile(r'/course/view\.php\?id=\d+'))
    courses_found = []
    
    for link in course_links:
        href = link['href']
        if "id=1" not in href: # Skip site home
            text = link.get_text().strip()
            if text and text not in courses_found:
                courses_found.append((text, href))

    if courses_found:
        print(f"  [OK] Found {len(courses_found)} Enrolled Courses:")
        for name, url in list(set(courses_found))[:5]: # Show top 5
             print(f"    - {name} ({url})")
        return courses_found
    else:
        print("  [X] No courses found on Dashboard. Warning: Student might not be enrolled!")
        return []

def verify_student_profile(session):
    print("\n=== 2. Verifying Student Profile ===")
    profile_url = f"{BASE_URL}/user/profile.php"
    resp = session.get(profile_url)
    
    if resp.status_code == 200 and "User details" in resp.text:
         print("  [OK] Profile page loaded successfully.")
         soup = BeautifulSoup(resp.text, 'html.parser')
         name = soup.find('h1').get_text() if soup.find('h1') else "Unknown"
         print(f"  [OK] Student Name Verified: {name}")
    else:
         print("  [X] Failed to load profile or 'User details' missing.")

if __name__ == "__main__":
    try:
        s = get_authenticated_session()
        if s:
            verify_student_dashboard(s)
            verify_student_profile(s)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
