# LMS Test Configuration
# Centralized configuration for all automation scripts

BASE_URL = "https://lms-demo.intelsoft.sg"

# Roles & Credentials (Demo Environment)
CREDENTIALS = {
    "admin": {
        "username": "admin",
        "password": "Password@123"
    },
    "manager": {
        "username": "manager_user", # To be created/verified
        "password": "Password@123"
    },
    "teacher": {
        "username": "teacher_user", # To be created/verified
        "password": "Password@123"
    },
    "student": {
        "username": "student_user", # To be created/verified
        "password": "Password@123"
    }
}

# Endpoints
ENDPOINTS = {
    "login": "/login/index.php",
    "dashboard": "/my/",
    "user_create": "/admin/user.php", # POST target for manual creation equivalent
    "course_manage": "/course/management.php",
    "course_edit": "/course/edit.php",
    "ajax_service": "/lib/ajax/service.php", # Moodle AJAX API
    "live_logs": "/report/loglive/index.php"
}

# Test Data Constants
TEST_COURSE_NAME = "E2E Automation Course"
TEST_COURSE_SHORTNAME = "E2E_AUTO_001"
TEST_CATEGORY_ID = 2 # Default 'Miscellaneous' or existing category
