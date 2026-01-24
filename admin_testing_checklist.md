# Admin End-to-End Verification Checklist

**Objective**: Verify the core functionality of the Admin account on the new AWS environment, ensuring no regression in User Management, Course Management, or System Administration.
**Environment**: `https://lms-demo.intelsoft.sg/`
**Tester**: [User Name]
**Date**: 2026-01-23

## 1. Authentication & Navigation

- [x] **Admin Login** (Verified by Automation):
  - **Action**: Login at `/login/index.php` using Admin credentials.
  - **Verify**: Redirects to Dashboard `/my/`. No errors (e.g., "Invalid login").
- [x] **Top Navigation Bar** (Verified by Script):
  - **Action**: Verify the finding of the following links:
    - `Home`, `Dashboard`, `My courses`, `Site administration`, `IOMAD dashboard`.
  - **Verify**: All links are clickable and lead to the correct pages.
- [FAIL] **Footer** (Verified by Script):
  - **Verify**: Footer contains "Powered by Moodle" and is valid (no "Lorem Ipsum").
  - **Note**: "Powered by Moodle" text is missing. "Lorem Ipsum" is NOT present. See Issue #18.

## 2. User Management (Critical)

**URL**: `/admin/user.php` (Browse list of users)

- [x] **Browse Users** (Verified by Automation):
  - **Action**: Go to `Site administration > Users > Accounts > Browse list of users`.
  - **Verify**: Table loads populated with users (Admin, Op User, De User, etc.).
- [x] **Filter Users** (Verified by Browser):
  - **Action**: Use "Add condition" -> "Email" -> contains "admin".
  - **Verify**: Table updates to show only the matching user.
- [x] **Check User Profile** (Verified by Script):
  - **Action**: Click on a user's name (e.g., `op_user`).
  - **Verify**: Profile page loads with "Edit profile" link available.

## 3. Course Management

**URL**: `/course/management.php`

- [x] **Category Listing** (Verified by Automation):
  - **Action**: Go to `Site administration > Courses > Manage courses and categories`.
  - **Verify**: Categories (e.g., "Medical", "General") are listed on the left.
- [x] **Create New Course** (Verified by Browser):
  - **Action**: Click "Create new course" (Right side).
  - **Data**: Full Name="AWS Check Course", Short Name="AWS001".
  - **Verify**: Course is successfully saved and you are redirected to "Course content" (or "Participants").
- [FAIL] **Course Search** (Verified by Browser):
  - **Action**: In the Search bar (top right), type "Ophthalmology".
  - **Verify**: Search results page `/course/search.php` loads relevant courses.
  - **Note**: No results found for "Ophthalmology" or "Ophthal". See Issue #19.

## 4. IOMAD / Multi-Tenancy (Unique to Intelsoft)

**URL**: `/blocks/iomad_company_admin/index.php`

- [x] **Company Dashboard** (Verified by Automation):
  - **Action**: Click "IOMAD dashboard" in top nav.
  - **Verify**: Dashboard loads with Company List (Ministry of Education, MOH, Dermatology, etc.).
- [x] **Company Switching** (Verified by Browser):
  - **Action**: Use the "Intelsoft" dropdown (top right) to switch view to "Dermatology".
  - **Verify**: Interface context changes (logo might change/banner update).
- [x] **Package Management** (Verified by Script):
  - **Action**: Verify presence of License/Package management links in IOMAD Dashboard.
  - **Verify**: Found 'License management', 'User license allocations', and 'Report' links.

## 5. Site Administration & System Health

**URL**: `/admin/search.php`

- [x] **Admin Search** (Verified by Automation):
  - **Action**: Type "Notifications" in the Admin Search bar.
  - **Verify**: Results show "Notifications" settings link.
- [x] **Notifications Check** (Verified by Automation):
  - **Action**: Click the Bell Icon (Top Right).
  - **Verify**: Popup opens. Click "See all" -> `/message/output/popup/notifications.php`. Ensure no 500/404 errors.
- [x] **Plugins Overview** (Verified by Automation):
  - **Action**: Go to `/admin/plugins.php` (or search "Plugins overview").
  - **Verify**: Page loads. Check for any "Missing from disk" or "Error" red flags.

## 6. Reporting

- [x] **Live Logs** (Verified by Automation):
  - **Action**: Go to `Site administration > Reports > Live logs`.
  - **Verify**: Page loads showing recent activity (including your own login).

---

**Defect Logging**:
If any test fails, please:

1.  Take a **Screenshot**. 📸
2.  Note the **Error Message**.
3.  Add it to `issue_report.md`.
