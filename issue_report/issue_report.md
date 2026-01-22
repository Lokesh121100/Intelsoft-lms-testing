# Intelsoft LMS Testing - Issue Report

## Issue #1: Certificates Display - "Nothing to Display" Error

| Field        | Details                            |
| ------------ | ---------------------------------- |
| **Severity** | Medium                             |
| **Location** | My Courses → Download Certificates |
| **Status**   | Open                               |

### Description

The "Download certificates" section displays "Nothing to display" message even when the user is enrolled in multiple courses (60 courses visible in the system).

### Expected Result

- If courses are completed: Certificates should be available for download
- If no courses completed: A clear message like "No certificates earned yet - complete a course to earn certificates"

### Actual Result

Shows "Nothing to display" with no additional context or guidance for the user.

### Screenshot

![Issue 1 - Certificates Nothing to Display](assets/issue_certificates_nothing_to_display.png)

---

## Issue #2: SCORM Content Loading with Play Button

| Field        | Details                              |
| ------------ | ------------------------------------ |
| **Severity** | High                                 |
| **Location** | CAP Initial Training → SCORM Package |
| **Status**   | Open                                 |

### Description

When accessing SCORM training content, the course displays a persistent loading state with a play button overlay, indicating content may not be loading properly.

### Expected Result

SCORM content should load automatically and begin playing without requiring additional user interaction, or clearly indicate loading progress.

### Actual Result

Content appears stuck with a play button overlay on a dark background, potentially indicating media loading issues.

### Screenshot

![Issue 2 - SCORM Content Loading](assets/issue_scorm_loading.png)

---

## Issue #3: SCORM Media Blocking (Content Security Policy)

| Field        | Details                 |
| ------------ | ----------------------- |
| **Severity** | High                    |
| **Location** | SCORM Training Packages |
| **Status**   | Open                    |

### Description

Browser console logs reveal that audio/video files embedded in SCORM packages using base64 encoding are being blocked by the Content Security Policy (CSP).

### Error Message

```
Loading media from 'data:audio/mp3;base64,...' violates the following
Content Security Policy directive: "media-src 'self' blob: https://intelsoft.info"
```

### Expected Result

All media content within SCORM packages should play without CSP restrictions.

### Actual Result

Audio and video content fails to play due to CSP blocking base64-encoded media sources.

### Recommended Fix

Update the Content Security Policy to allow `data:` sources for media:

```
media-src 'self' blob: data: https://intelsoft.info
```

---

## Issue #4: Font Decoding Errors

| Field        | Details   |
| ------------ | --------- |
| **Severity** | Low       |
| **Location** | Site-wide |
| **Status**   | Open      |

### Description

Multiple console errors indicate that custom fonts are failing to decode properly.

### Error Messages

```
Failed to decode downloaded font: https://intelsoft.info/theme/font.php/.../OpenSans-Bold.ttf
Failed to decode downloaded font: https://intelsoft.info/theme/font.php/.../OpenSans-Regular.ttf
```

### Expected Result

Fonts should load and render correctly throughout the platform.

### Actual Result

Font files fail to decode, potentially causing inconsistent typography or fallback to system fonts.

---

## Issue #5: Private Files Section - Loading State

| Field        | Details                    |
| ------------ | -------------------------- |
| **Severity** | Low                        |
| **Location** | User Menu → Private Files  |
| **Status**   | Open (Verified 4-5s delay) |

### Description

The Private Files section file manager consistently displays a "Loading..." spinner for approximately 4-5 seconds before becoming interactive, creating a sluggish user experience.

### Screenshot

![Issue 5 - Private Files Section](assets/private_files_loading_bug_1769023422228.png)

---

## Issue #6: Placeholder Text on Manager Dashboard Banner

| Field         | Details                    |
| ------------- | -------------------------- |
| **Severity**  | Medium                     |
| **Location**  | Manager Dashboard → Banner |
| **User Role** | Manager                    |
| **Status**    | Open                       |

### Description

While reviewing the Manager dashboard, placeholder text "Lorem ipsum dolor sit amet…" is displayed in the banner section. This appears to be dummy content and is not meaningful for end users.

### Expected Result

Meaningful and relevant content (such as welcome message, announcements, or platform information) should be displayed instead of placeholder text.

### Actual Result

The banner displays Lorem ipsum placeholder text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."

### Screenshot

![Issue 6 - Lorem Ipsum Placeholder](assets/issue_lorem_ipsum_placeholder.png)

---

## Issue #7: Course Search System Error

| Field         | Details                            |
| ------------- | ---------------------------------- |
| **Severity**  | Critical                           |
| **Location**  | Manager → Courses → Search courses |
| **User Role** | Manager                            |
| **Status**    | Open                               |

### Description

While testing the Search courses feature in the Manager account, the system fails to return results when a valid course name is searched. Instead, it redirects to an error page and displays a system exception message, exposing a backend error to the user.

### Expected Result

The system should display matching course results or a user-friendly message if no courses are found (e.g., "No courses found matching your search").

### Actual Result

The system displays an error message:

```
Exception – Call to a member function get_formatted_name() on null
```

No search results are shown, and the backend exception is exposed to the user.

### Screenshots

**Search Page (before error):**
![Course Search Page](assets/issue_course_search_page.png)

**Error Page:**
![Issue 7 - Course Search Error](assets/issue_course_search_error.png)

---

## Additional Observations

### Course Management Interface

The My Courses interface displays with proper functionality. User management, course groups, and learning paths are accessible.

![My Courses View](assets/issue_my_courses_view.png)

### Course Content Page

CAP Initial Training course content page shows proper structure with SCORM package, Reports, and More tabs.

![Course Content Structure](assets/issue_course_content.png)

---

## Testing Session Recording

A complete video recording of the testing session is available:

![Testing Session Recording](assets/dashboard_exploration_1769023067975.webp)

---

## Issue #8: Public Homepage Placeholder Content (NEW - Public Access)

| Field        | Details                                  |
| ------------ | ---------------------------------------- |
| **Severity** | High                                     |
| **Location** | Public Homepage (https://intelsoft.info) |
| **Status**   | Open                                     |

### Description

The public homepage displays Lorem ipsum placeholder text in the slideshow banners, which is unprofessional and indicates incomplete content setup.

### Homepage Content Analysis

**Slideshow Banners (All 3 banners show identical placeholder text):**

```
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
```

### Expected Result

- Professional, relevant content about the LMS platform
- Information about courses, features, or company services
- No placeholder text visible to the public

### Actual Result

- Lorem ipsum placeholder text prominently displayed
- Unprofessional appearance for public visitors
- Content appears incomplete or under development

### Public Access Concern

The homepage is accessible without login, meaning any internet user can see this placeholder content.

### Screenshot

![Issue 8 - Public Homepage Placeholder](assets/issue_public_homepage_placeholder.png)

---

## Issue #9: Missing Course Progress Indicators

| Field        | Details                |
| ------------ | ---------------------- |
| **Severity** | Medium                 |
| **Location** | Dashboard & My Courses |
| **Status**   | Open                   |

### Description

Course cards on the Dashboard and "My Courses" page fail to display any visual progress indicators (e.g., progress bars or "X% complete" text), even for active courses. The dashboard summary explicitly states "0 Courses completed" and "0 Activities completed" despite ongoing activity.

### Expected Result

Active courses should display a progress bar or percentage to indicate the user's advancement through the material.

### Actual Result

No progress information is visible on course cards, leaving users unaware of their standing.

### Screenshot

![Issue 9 - Missing Progress Indicators](assets/issue_missing_progress_indicators.png)

---

## Issue #10: Unclear Activity Completion Tracking

| Field        | Details              |
| ------------ | -------------------- |
| **Severity** | Medium               |
| **Location** | Course Content Pages |
| **Status**   | Open                 |

### Description

Inside courses (e.g., "Fundamentals of Python Programming"), there are no manual "Mark as done" buttons or clear visual confirmations when an activity is completed.

### Expected Result

Users should have clear feedback (checkboxes, "Done" labels, or manual toggle buttons) to track which activities they have completed.

### Actual Result

Activity completion status is invisible or missing, making self-pacing difficult.

### Screenshot

![Issue 10 - Unclear Activity Completion](assets/issue_unclear_activity_completion.png)

---

## Issue #11: Grade Report System Warning

| Field        | Details            |
| ------------ | ------------------ |
| **Severity** | High               |
| **Location** | User Menu → Grades |
| **Status**   | Open               |

### Description

When accessing the Grade Report for a specific course, a critical system warning is displayed: "Warning: Activity deletion in progress! Some grades are about to be removed."

### Expected Result

Grade reports should display student grades cleanly without exposing backend maintenance warnings to end users.

### Actual Result

Users are presented with an alarming warning message suggesting data loss or system instability.

### Screenshot

![Issue 11 - Grade Report Warning](assets/issue_grade_report_warning.png)

---

## Issue #12: Manager Role Permissions Missing (Add Course / Site Admin)

| Field        | Details                         |
| ------------ | ------------------------------- |
| **Severity** | Critical                        |
| **Location** | Dashboard / Site Administration |
| **Status**   | Open                            |

### Description

The user logged in as "Manager" (`sandboxcm`) lacks critical permissions expected for this role.

1.  **Missing "Add Course" functionality**: There is no button to create new courses.
2.  **Missing "Site Administration"**: The administration block is completely absent.

### Expected Result

A Manager should be able to create new courses and access relevant Site Administration settings for course/user management.

### Actual Result

The user is restricted to viewing existing courses without creation capabilities, rendering the "Manager" role ineffective.

### Screenshot

![Issue 12 - Missing Add Course Button](assets/issue_manager_no_add_course.png)

---

## Issue #13: Missing Edit Mode & Enrollment Controls

| Field        | Details                    |
| ------------ | -------------------------- |
| **Severity** | High                       |
| **Location** | Course Page / Participants |
| **Status**   | Open                       |

### Description

Within a specific course (e.g., "CAP Initial Training"), the Manager is unable to perform basic management tasks:

1.  **Edit Mode Missing**: The "Edit mode" toggle (usually top right) is not available inside the course, preventing any content changes.
2.  **Enrol Users Missing**: The "Participant" tab lacks the standard "Enroll users" button.

### Expected Result

Managers must be able to:

- Toggle "Edit mode" to add/remove activities and resources.
- Manually enroll users into the course via the Participants tab.

### Actual Result

The interface is locked in "View only" mode for the Manager, similar to a Student view.

### Screenshots

**Missing Edit Mode:**
![Issue 13 - Missing Edit Mode](assets/issue_manager_no_edit_mode.png)

**Missing Enroll Button:**
![Issue 13 - Missing Enroll Button](assets/issue_manager_no_enroll_button.png)

---

## Summary Table

| Issue # | Description                        | Severity | Impact                       |
| ------- | ---------------------------------- | -------- | ---------------------------- |
| 1       | Certificates "Nothing to Display"  | Medium   | User confusion               |
| 2       | SCORM Content Loading State        | High     | Training access blocked      |
| 3       | CSP Blocking Media                 | High     | Audio/Video fails            |
| 4       | Font Decoding Errors               | Low      | Visual inconsistency         |
| 5       | Private Files Loading              | Low      | File management delay        |
| 6       | Lorem Ipsum Placeholder Text       | Medium   | Unprofessional appearance    |
| 7       | Course Search System Error         | Critical | Search functionality broken  |
| 8       | Public Homepage Placeholder        | High     | Unprofessional public image  |
| 9       | Missing Course Progress Indicators | Medium   | User loses track of progress |
| 10      | Unclear Activity Completion        | Medium   | Poor user experience         |
| 11      | Grade Report System Warning        | High     | User alarm/confusion         |
| 12      | Manager Permissions Missing        | Critical | Role is ineffective          |
| 13      | Edit Mode & Enrollment Missing     | High     | Cannot manage course content |

---

## Recommendations

1.  **Critical Priority:** Fix Course Search functionality (Issue #7) - backend null reference error
2.  **Critical Priority:** Restore "Manager" permissions (Issue #12 & #13) to allow course creation and editing.
3.  **Immediate Priority:** Fix CSP policy to allow SCORM media content
4.  **High Priority:** Turn off debug/maintenance warnings in Grade Reports (Issue #11)
5.  **High Priority:** Replace public homepage Lorem ipsum placeholder text (Issue #8)
6.  **High Priority:** Investigate SCORM content loading issues
7.  **Medium Priority:** Enable visual progress bars on course cards (Issue #9)
8.  **Medium Priority:** Replace manager dashboard Lorem Ipsum text with meaningful content (Issue #6)
9.  **Medium Priority:** Add clearer messaging for empty certificate states
10. **Low Priority:** Fix font file serving configuration

## Issue #14: Public Site Issues (Guest View)

| Field        | Details                        |
| ------------ | ------------------------------ |
| **Severity** | High                           |
| **Location** | Homepage, Course Pages, Footer |
| **Status**   | Open                           |

### Description

A public audit of `lms-demo.intelsoft.sg` revealed significant incomplete content visible to unauthenticated guests.

1.  **Homepage Placeholders:** "Lorem ipsum" text is prominently displayed in the main sliders.
2.  **Broken Technical Tags:** The Course Enrolment page displays raw code tags `[[nocourseduration]]` instead of the course duration.
3.  **Empty Footer:** The footer lacks standard links (Privacy Policy, Contact, Terms), showing a bare layout.

### Expected Result

- Homepage should contain real marketing copy.
- Technical tags should render actual values or be hidden.
- Footer should contain legal and contact links.

### Actual Result

- "Lorem ipsum" visible to public.
- `[[nocourseduration]]` visible to public.
- Footer is empty.

### Recommended Fix

1.  **Content**: Provide and upload final text for homepage banners.
2.  **Development**: Debug the `[[nocourseduration]]` shortcode in the course page template.
3.  **Layout**: Add "Contact Us" and "Privacy Policy" pages and link them in the footer.

- "Lorem ipsum" visible to public.
- `[[nocourseduration]]` visible to public.
- Footer is empty.

### Screenshots

**Guest Homepage (Lorem Ipsum):**
![Guest Homepage Issue](assets/guest_homepage_view_1769102456042.png)

**Broken Duration Tag:**
![Broken Duration Tag](assets/course_enrolment_guest_view_1769102689688.png)

---

## Issue #15: Notification System Error & Guest Access Bug

| Field        | Details                            |
| ------------ | ---------------------------------- |
| **Severity** | High                               |
| **Location** | Top Navigation Bar → Notifications |
| **Status**   | Open                               |

### Description

When clicking the Notification icon in the top navigation bar:

1.  The popup displays a persistent loading spinner and fails to load content.
2.  Clicking "See all" redirects to an error page stating "Guest user can not edit messaging options", which is an incorrect context for viewing notifications.

### Actual Result

- **Popup:** stuck on loading spinner.
- **See All:** Error message "Guest user can not edit messaging options".

### Expected Result

- Notifications should load relevant alerts or "No notifications" state.
- "See all" should take the user to a full notifications page, or prompt for login if access is restricted (not an editing permission error).

### Screenshots

**Loading Spinner:**
![Notification Loading Issue](assets/issue_notification_loading_spinner.png)

**Guest Error Message:**
![Notification Guest Error](assets/issue_notification_guest_error.png)

---

## Issue #16: Empty Course Category Listings

| Field        | Details                                    |
| ------------ | ------------------------------------------ |
| **Severity** | High                                       |
| **Location** | Courses → Category View (e.g. Pulmonology) |
| **Status**   | Open                                       |

### Description

When navigating to a specific course category (e.g., "Pulmonology") or searching for courses, the content area displays as completely empty. The category title is visible, but no courses are listed, even though the side menu structure suggests categories exist.

### Actual Result

- **Content Area:** Completely blank white space under the category dropdown.
- **Sidebar:** Categories are listed, but selecting one shows no content.

### Expected Result

- The page should display a grid or list of courses available within the selected category.
- If no courses exist, a clear "No courses available in this category" message should be displayed.

### Screenshot

**Empty Category View:**
![Empty Course Category](assets/issue_empty_course_category.png)
