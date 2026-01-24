
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lms-demo.intelsoft.sg"
LOGIN_URL = f"{BASE_URL}/login/index.php"
USERS_URL = f"{BASE_URL}/admin/user.php"
USERNAME = "admin"
PASSWORD = "Password@123"

def list_users():
    session = requests.Session()
    # Login
    resp = session.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    token = soup.find('input', {'name': 'logintoken'})['value']
    session.post(LOGIN_URL, data={'username': USERNAME, 'password': PASSWORD, 'logintoken': token})
    
    # Get Users
    resp = session.get(USERS_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Print ID, First/Last, Email from table
    rows = soup.select('table#users tbody tr')
    print(f"Found {len(rows)} users. Listing first 10:")
    for row in rows[:20]:
        cols = row.find_all('td')
        if len(cols) > 3:
            name = cols[0].get_text(strip=True)
            email = cols[1].get_text(strip=True)
            print(f"User: {name} | Email: {email}")

if __name__ == "__main__":
    list_users()
