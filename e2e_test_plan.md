# LMS End-to-End (E2E) Automation Test Plan

**Objective**: Validate core functionalities, UI behavior, permissions, and data consistency across all roles (Admin, Manager, Teacher, Student) for the Iomad-based LMS.
**Target URL**: `https://lms-demo.intelsoft.sg/`

## 1. Authentication & Roles

| ID  | Test Case      | Role                             | Expected Result                |
| --- | -------------- | -------------------------------- | ------------------------------ |
| 1.1 | Login Success  | Admin, Manager, Teacher, Student | Dashboard loads successfully.  |
| 1.2 | Logout Success | All                              | Redirected to Login page.      |
| 1.3 | Invalid Login  | -                                | Error message displayed.       |
| 1.4 | Role Access    | Student                          | Cannot access `/admin/` pages. |

## 2. IOMAD Dashboard

| ID  | Test Case      | Role          | Expected Result                                   |
| --- | -------------- | ------------- | ------------------------------------------------- |
| 2.1 | Dashboard Load | Admin/Manager | Widgets, counts, and graphs verify against DB.    |
| 2.2 | Company Switch | Admin         | Dashboard data updates based on selected company. |

## 3. Course Management

| ID  | Test Case      | Role          | Expected Result                                |
| --- | -------------- | ------------- | ---------------------------------------------- |
| 3.1 | Create Course  | Admin/Manager | Course created with "Manual" enrolment.        |
| 3.2 | Assign Company | Admin         | Course visible only to assigned Company users. |
| 3.3 | Edit Course    | Admin/Teacher | Changes to Summary/Name persist.               |
| 3.4 | Delete Course  | Admin         | Course removed from list.                      |

## 4. Package Management (Iomad)

| ID  | Test Case        | Role  | Expected Result                                       |
| --- | ---------------- | ----- | ----------------------------------------------------- |
| 4.1 | View Packages    | Admin | List of packages loads.                               |
| 4.2 | Assign Package   | Admin | Company license count decreases/updates.              |
| 4.3 | Validate Mapping | Admin | Courses in package are accessible to allocated users. |

## 5. User Management & Participants

| ID  | Test Case           | Role          | Expected Result                                            |
| --- | ------------------- | ------------- | ---------------------------------------------------------- |
| 5.1 | Create User         | Admin/Manager | User can login with set credentials.                       |
| 5.2 | Assign Role         | Admin         | User has correct permissions (e.g., Teacher capabilities). |
| 5.3 | Enrol User          | Manager       | User appears in Course Participants list.                  |
| 5.4 | Filter Participants | Teacher       | Filter by "First Name" works correctly.                    |

## 6. Learning Flow

| ID  | Test Case         | Role         | Expected Result                    |
| --- | ----------------- | ------------ | ---------------------------------- |
| 6.1 | Open Course       | Student      | Course content (SCORM/Quiz) loads. |
| 6.2 | Complete Activity | Student      | Progress bar updates to 100%.      |
| 6.3 | Last Access       | Admin/Report | Log shows recent access timestamp. |

## 7. UI & Error Handling

| ID  | Test Case     | Role | Expected Result                               |
| --- | ------------- | ---- | --------------------------------------------- |
| 7.1 | Broken Links  | All  | No 404/500 errors on main nav.                |
| 7.2 | Button States | All  | "Save" disabled until required fields filled. |
