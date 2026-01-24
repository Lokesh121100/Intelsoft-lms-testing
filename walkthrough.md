# Testing Session Walkthrough

**Date:** 2026-01-23
**Environment:** `lms-demo.intelsoft.sg` (AWS)

## Summary of Work

We conducted a comprehensive testing session coverage both **Manual Discovery** and **Automated Issue Hunting**.

### 1. Phase 1: Deep Crawl (Data Collection)

- **Discovery**: Identified the system as **IOMAD** (Enterprise Moodle).
- **Inventory**: Mapped 100+ pages including Commerce, Safe Exam Browser, and Company Admin.
- **Outcome**: Populated `feature_inventory.md`.

### 2. Phase 3: AWS Verification & Departmental Isolation

We performed **Live Browser Verification** on the new AWS environment.

**1. Ophthalmology User (`op_user`)**:

- **Status**: **PASS (Verified)**
- **Isolation**: Visible "Ophthalmology" content. Hidden "Dermatology" content.
- **Evidence**: `assets/ophthalmology_dashboard_1769157285347.png`.

**2. Dermatology User (`de_user`)**:

- **Status**: **PASS (Verified)**
- **Isolation**: Visible "Dermatology" content. Hidden "Ophthalmology" content.
- **Evidence**: `assets/dermatology_user_courses_1769159705970.png`.

**3. Admin Login**:

- **Status**: **Verified Manually**. (Automated scripts blocked by enhanced Bot Detection on AWS).

## Deliverables

- [Feature Inventory](file:///f:/Intelsoft-lms-testing/feature_inventory.md)
- [Evidence: Op User Dashboard](file:///f:/Intelsoft-lms-testing/assets/ophthalmology_dashboard_1769157285347.png)
- [Evidence: De User Dashboard](file:///f:/Intelsoft-lms-testing/assets/dermatology_user_courses_1769159705970.png)
