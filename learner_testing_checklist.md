# Learner Role Testing Checklist (sandboxlearner2)

**Objective:** Verify all student-facing features on `lms-demo.intelsoft.sg`.

## 1. Authentication & Profile

- [x] **Login** (Verified by Script): Verify login with `demolearner@moe.gov.sg` / `Password@123`.
- [x] **Dashboard** (Verified by Script): Check if enrolled courses are visible (Result: Dashboard loads, but courses not listed).
- [x] **Profile** (Verified by Script): Try to update profile picture or description (Verified Read Access).
- [ ] **Notifications**: Check if the notification bell works (given Issue #15).

## 2. Course Engagement

- [ ] **Course Access**: Open a specific course (Result: Failed to access directly).
- [ ] **Content Navigation**: Click through sections/modules.
- [ ] **Completion Tracking**: Verify if "Mark as done" buttons or checkboxes work.
- [ ] **Resource Access**: Download a PDF or view a page.

> **Note**: Course access failed despite valid enrollment. Logged as Issue #20.

## 3. Assessments

- [ ] **Assignment Submission:** Attempt to submit a file to an assignment.
- [ ] **Quiz:** Attempt a quiz attempt (start, answer, submit).
- [ ] **Grades:** Check the "Grades" section for visibility.

## 4. Communication

- [ ] **Messaging:** Try to send a message to a teacher/manager.
- [ ] **Forum:** Post in a discussion forum (if available).

## 5. Feature Inventory & Discovery

- [ ] **Document All Features:** List every available menu item, button, and capability found during testing.
- [ ] **Unexpected Features:** Note any features that seem out of place for a student role.

**Status:** Ready to start.
