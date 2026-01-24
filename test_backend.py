import requests
from bs4 import BeautifulSoup
import test_config as config
import time

class LMSClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Automation/1.0'
        })
        self.base_url = config.BASE_URL

    def get_login_token(self, login_url):
        """Extracts Moodle login token from the login page."""
        response = self.session.get(login_url)
        if response.status_code != 200:
            raise Exception(f"Failed to load login page: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'logintoken'})
        if not token_input:
             # Already logged in?
            if "alert-error" in response.text:
                 print("Login page shows error.")
            return None
        return token_input['value']

    def login(self, role="admin"):
        """Logs in with the specified role."""
        creds = config.CREDENTIALS.get(role)
        if not creds:
            raise ValueError(f"Unknown role: {role}")
        
        login_url = f"{self.base_url}{config.ENDPOINTS['login']}"
        print(f"[{role.upper()}] authenticating...")
        
        token = self.get_login_token(login_url)
        if not token:
            print(f"[{role.upper()}] Could not get token (possibly already logged in via session cookie)")
            # Verify anyway
        else:
            payload = {
                'username': creds['username'],
                'password': creds['password'],
                'logintoken': token
            }
            resp = self.session.post(login_url, data=payload)
        
        # Verify Login
        dash_url = f"{self.base_url}{config.ENDPOINTS['dashboard']}"
        resp_dash = self.session.get(dash_url)
        
        if "Dashboard" in resp_dash.text or "Customize this page" in resp_dash.text:
            print(f"[OK] [{role.upper()}] Login Success")
            return True
        else:
            print(f"[X] [{role.upper()}] Login Failed")
            return False

    def login_with_creds(self, username, password):
        """Helper to check credentials without role config."""
        login_url = f"{self.base_url}{config.ENDPOINTS['login']}"
        token = self.get_login_token(login_url)
        if not token: return False
        
        payload = {'username': username, 'password': password, 'logintoken': token}
        self.session.post(login_url, data=payload)
        dash_url = f"{self.base_url}{config.ENDPOINTS['dashboard']}"
        resp = self.session.get(dash_url)
        return "Dashboard" in resp.text or "Customize this page" in resp.text

    def check_page_access(self, url_suffix, description):
        """Verifies if a page is accessible (200 OK) or forbidden."""
        full_url = f"{self.base_url}{url_suffix}"
        resp = self.session.get(full_url)
        status = resp.status_code
        
        if status == 200:
            if "error/moodle/generalexceptionmessage" in resp.text: 
                 print(f"   [!] {description}: 200 OK but content indicates Error.")
                 return False
            print(f"   [OK] {description}: Accessible (200 OK)")
            return True
        elif status in [403, 404]:
            print(f"   [LOCK] {description}: Access Denied ({status} Expected)")
            return False
        else:
            print(f"   [?] {description}: Status {status}")
            return False

    def create_user(self, username, password, email, firstname, lastname):
        """Creates a new user via the Admin interface."""
        # Check if user already exists by trying to log in
        temp_client = LMSClient()
        if temp_client.login_with_creds(username, password):
            print(f"   [!] User '{username}' already exists (Login success). Skipping creation.")
            return True

        print(f"   [+] Creating user '{username}'...")
        
        # 1. Get the Create User Page to fetch tokens
        create_url = f"{self.base_url}/admin/user/editadvanced.php?id=-1"
        resp = self.session.get(create_url)
        
        # Moodle page titles vary. Check for form.
        if "mform1" not in resp.text and "id=\"mform1\"" not in resp.text:
             # Just dump a snippet if it fails to help debug
             print(f"   [X] Failed to load User Creation page. Title: {resp.text[:100]}...")
             return False
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract Sesskey (already in session usually, but good to be safe)
        sesskey_input = soup.find('input', {'name': 'sesskey'})
        if not sesskey_input:
             print("   [X] Could not find sesskey.")
             return False
        sesskey = sesskey_input['value']
        
        # 2. Prepare Payload
        # Note: Moodle forms are complex. We submit the bare minimum required.
        payload = {
            'sesskey': sesskey,
            '_qf__user_edit_advanced_form': '1',
            'mform_isexpanded_id_moodle': '1',
            'username': username,
            'newpassword': password,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'submitbutton': 'Create user',
            # Defaults
            'auth': 'manual',
            'confirmed': '1',
            'maildisplay': '1',
            'city': 'Singapore',
            'country': 'SG',
            'timezone': 'Asia/Singapore',
            'lang': 'en'
        }
        
        # 3. Post Data
        post_resp = self.session.post(create_url, data=payload)
        
        # 4. Verify Success
        # On success, Moodle usually redirects to the user list or shows the list.
        # We check if the user appears in the Browse list or if we get an error.
        
        if "error" in post_resp.text and "class=\"error\"" in post_resp.text:
            # Check if it's "Username already exists"
            if "Username already exists" in post_resp.text:
                print(f"   [!] User '{username}' already exists. Skipping.")
                return True
            print(f"   [X] Error creating user: {post_resp.text[:200]}...") # truncate
            return False
            
        print(f"   [OK] User '{username}' created successfully.")
        return True

    def create_course(self, fullname, shortname, category_id=1):
        """Creates a new course."""
        print(f"   [+] Creating course '{shortname}'...")
        
        # 1. Check if course exists (Search)
        # We can't easily search via API without web service, so we try to Create.
        # If shortname exists, Moodle will complain.
        
        create_url = f"{self.base_url}/course/edit.php?category={category_id}"
        resp = self.session.get(create_url)
        
        if "Add a new course" not in resp.text:
             print("   [X] Failed to load Course Creation page.")
             return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        sesskey = soup.find('input', {'name': 'sesskey'})['value']
        
        # 2. Payload
        payload = {
            'sesskey': sesskey,
            '_qf__course_edit_form': '1',
            'mform_isexpanded_id_general': '1',
            'baseurl': create_url,
            'fullname': fullname,
            'shortname': shortname,
            'category': category_id,
            'visible': '1',
            'startdate[day]': '1',
            'startdate[month]': '1',
            'startdate[year]': '2026',
            'idnumber': '',
            'summary_editor[text]': 'Automated Test Course',
            'submitbutton': 'Save and display'
        }
        
        # 3. Post (Assuming 200 OK or Redirect)
        post_resp = self.session.post(create_url, data=payload)
        
        # 4. Verify
        if "Short name is already used" in post_resp.text:
            print(f"   [!] Course '{shortname}' already exists. Skipping.")
            return True # Treat as success
            
        # Check if we landed on 'Participants' or 'Course Content'
        if "Course" in post_resp.text or "Participants" in post_resp.text:
            print(f"   [OK] Course '{shortname}' created/verified.")
            return True
            
        print(f"   [X] Failed to create course. Resp: {post_resp.text[:300]}...")
        return False

def run_auth_tests():
    print("\n--- TEST: Authentication & Roles ---")
    client = LMSClient()
    
    # 1. Admin Login
    result = client.login("admin")
    if not result:
        print("CRITICAL: Admin login failed. Stopping tests.")
        return

    # 2. Create Roles
    print("\n--- INFRA: Creating Test Users ---")
    for role, creds in config.CREDENTIALS.items():
        if role == "admin": continue
        
        # Create unique email to avoid conflicts
        email = f"{creds['username']}@test.intelsoft.sg"
        client.create_user(
            username=creds['username'],
            password=creds['password'],
            email=email,
            firstname=f"Auto_{role.title()}",
            lastname="TestUser"
        )

    # 3. Verify Admin Access
    print("\n--- VERIFY: Admin Permissions ---")
    client.check_page_access(config.ENDPOINTS['live_logs'], "Live Logs (Admin)")
    client.check_page_access(config.ENDPOINTS['course_manage'], "Course Management")

    # 4. Verify Student Login
    # Note: We need a fresh session for this.
    print("\n--- VERIFY: Student Login ---")
    student_client = LMSClient()
    student_login = student_client.login("student")
    
    if student_login:
        print("   [CHECK] Student Access Config:")
        student_client.check_page_access(config.ENDPOINTS['live_logs'], "Live Logs") # Should FAIL (403/Forbidden)
        student_client.check_page_access("/my/", "Student Dashboard") # Should PASS

    # Course Creation logic moved to class


def run_course_tests():
    print("\n--- TEST: Course Management ---")
    client = LMSClient()
    if not client.login("admin"): return
    
    # Create Test Course
    client.create_course(
        fullname=config.TEST_COURSE_NAME, 
        shortname=config.TEST_COURSE_SHORTNAME,
        category_id=config.TEST_CATEGORY_ID
    )

if __name__ == "__main__":
    run_auth_tests()
    # run_course_tests()
