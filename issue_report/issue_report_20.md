## Issue #20: Student Course Access Failure (Critical)

**Priority:** High
**Role:** Student (Learner)
**Status:** Open

### Description

After a Student is enrolled in a course (e.g., "AWS Check Course"), the course **does not appear** on their Dashboard. Attempting to access the course directly by URL redirects or shows an "Enrol me" page, indicating the system does not recognize the enrollment.

### Steps to Reproduce

1. Log in as Admin.
2. Enrol a user (e.g., `demolearner@moe.gov.sg`) into `AWS Check Course` as "Student".
3. Log out and Log in as `demolearner@moe.gov.sg`.
4. Check "My courses" on Dashboard.
5. Attempt to access `/course/view.php?id=[ID]`.

### Expected Result

- Course should appear on the Dashboard cards.
- Direct link should open the Course Home Page.

### Actual Result

- Dashboard shows "No courses found".
- Direct link requests enrollment ("Enrol me") again.

### Evidence

- **Verification Script Log**: `[X] No courses found on Dashboard.`
- **Enrollment Confirmation**: Admin panel shows user is enrolled (Active).
