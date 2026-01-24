
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lms-demo.intelsoft.sg"
LOGIN_URL = f"{BASE_URL}/login/index.php"
USERNAME = "admin"
PASSWORD = "Password@123"

def get_course_id():
    session = requests.Session()
    session.post(LOGIN_URL, data={'username': USERNAME, 'password': PASSWORD})
    
    # Search for course
    search_url = f"{BASE_URL}/course/search.php?q=AWS Check Course"
    resp = session.get(search_url)
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if 'course/view.php?id=' in href and 'AWS Check Course' in link.get_text():
            print(f"FOUND COURSE ID: {href}")
            return
            
    print("Course not found via search.")

if __name__ == "__main__":
    get_course_id()
