# Testing Session Walkthrough

**Date:** January 22, 2026
**Environment:** `lms-demo.intelsoft.sg`

## Summary of Work

We conducted a comprehensive testing session covering both Public (Guest) and Learner (Student) roles.

### 1. Verified Public & Guest Issues

- Confirmed "Lorem Ipsum" placeholder text on homepage.
- Identified broken `[[nocourseduration]]` tags on course pages.
- Verified empty footer links.
- **Outcome:** Documented in Issue #14.

### 2. Tested Learner Role (`sandboxlearner2`)

- **Login:** Successful with `Changeme!1`.
- **Feature Inventory:** Verified Dashboard, Grades, Profile, Private Files.
- **Coursework:** Successfully submitted an assignment file and attempted a quiz.
- **Notifications:** Confirmed notifications work correctly (no spinner error for this role).

### 3. Reporting

- **Issue Report:** Consolidated 16 issues into `issue_report.md`.
- **PDF Generation:** Created a Python script (`generate_pdf.py`) to generate a high-quality PDF report with full-width screenshots.
- **Final Deliverable:** `Intelsoft_LMS_Issue_Report.pdf` (Cleaned of metadata header as requested).

## Deliverables

- [Issue Report Markdown](file:///f:/Intelsoft-lms-testing/issue_report/issue_report.md)
- [Issue Report PDF](file:///f:/Intelsoft-lms-testing/issue_report/Intelsoft_LMS_Issue_Report.pdf)
- [Learner Checklist](file:///f:/Intelsoft-lms-testing/learner_testing_checklist.md)
