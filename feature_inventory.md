# 📦 IntelSoft LMS - Feature Inventory & System Map

**Date:** 2026-01-23
**Environment:** `lms-demo.intelsoft.sg`
**System Type:** **IOMAD** (Enterprise Moodle Wrapper)

## 1. Core Architecture

| Component          | Status  | Details                                               |
| :----------------- | :------ | :---------------------------------------------------- |
| **System Core**    | IOMAD   | Multi-tenancy enabled (Company/Department structure). |
| **Theme**          | Custom  | "Intelsoft Info" branding.                            |
| **Language Packs** | English | Default.                                              |
| **Cron Status**    | Unknown | Needs Admin Check.                                    |

## 2. Activity Modules (Learning Tools)

_Detected via Crawler and Menu Links._

| Module                 | Enabled? | Notes / Config                                                  |
| :--------------------- | :------- | :-------------------------------------------------------------- |
| **Quiz**               | ✅       | **Safe Exam Browser (SEB)** templates are active.               |
| **IOMAD Company**      | ✅       | Company Admin Block (`blocks/iomad_company_admin`) is critical. |
| **Detailed Responses** | ?        | Needs manual check.                                             |

## 3. Local Plugins & Blocks

- **IOMAD Company Admin**: `/blocks/iomad_company_admin/` - The heart of the multi-tenancy system.
- **IOMAD Commerce**: `/blocks/iomad_commerce/shop.php` - E-commerce shop enabled.
- **Custom Reports**: `local/report_emails` - A custom plugin for "Outgoing Email Reports".
- **Teaching Locations**: `/blocks/iomad_company_admin/classroom_list.php` - Offline session management.

## 4. User & Authentication

| Method         | Enabled? | Notes                                      |
| :------------- | :------- | :----------------------------------------- |
| **IOMAD Auth** | ✅       | Company-based user assignment.             |
| **SingPass**   | ✅       | Detected `auth/oauth2/login.php` (OAuth2). |
| **Manual**     | ✅       | Admin can create users manually.           |

## 5. E-Commerce & Enrolment

- **Shop**: Active. Allows purchasing courses?
- **Licensing**: IOMAD usually handles licenses. Needs verification.

## 6. Data Collection & Analytics

- **Learning Plans**: Active (`admin/tool/lp/learningplans.php`). Competency frameworks are in use.
- **Outgoing Email Report**: A dedicated report for tracking system emails.

## 7. Known Issues (From Discovery)

- **Messaging System**: `message/index.php` triggers an "Error" page title.
- **Category Links**: Some category links (ID 4, 14) are broken/looping.
