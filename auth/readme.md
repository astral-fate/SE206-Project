## Chapter 3: Implementation

This chapter details the implementation phase of the Cairo University Platform, outlining the methodologies, user stories, product backlog, project estimations, and a comprehensive test plan.

### 3.1 Agile Methodology

The project adopted an Agile methodology, specifically incorporating principles of iterative development and estimation based on user stories. This approach allowed for flexibility and continuous adaptation throughout the development lifecycle, as evidenced by the "Iteration Planning" and "Story Size Estimation" frameworks utilized. The project embraced incremental delivery, with a planned total of 7 iterations, each aiming to deliver 25 story sizes, demonstrating a commitment to regular progress assessment and adjustment.

### 3.2 User Stories

User stories served as the core of the development process, capturing functional requirements from various perspectives: students and administrators. These stories were derived from the initial feature list and detailed use cases, guiding the development and testing efforts.

#### Feature List Over All Model

| ID | Feature List |
|---|---|
| 1 | As a new user, I can register an account so that I can access the platform's features. |
| 2 | As a registered user, I can log in to the platform to access my profile |
| 3, 4 | As a user, I can manage my profile and set permissions to protect my privacy. As a user, I can search for available Track based on my access. |
| 5 | As a user, I can view details about each available Track, including the Subjects and prices. |
| 6 | As a user, I can modify or cancel my bookings any time I need. |
| 7 | As a user, I am able to securely enter my payment information to complete a Registration. |
| 8 | As a user, I can receive a confirmation of my booking once the payment processed. |
| 9 | As a user, I can view ratings and feedback from the other users to help me making decisions about this Track. |

#### Plan By Feature

| Task | Project Schedule | Task Name | Owned By | Chief Programmer | Priority |
|---|---|---|---|---|---|
| 1 | Day 1-5 | User Registration | Abdulrahman | Fatimah | High |
| 2, 3 | Day 6-9, Day 10-15 | User Login, Track View and Registration | Hanouf, Hany | Fatimah, Ahmed | High, High |
| 4 | Day 16-19 | Registration MGMT | Hanouf | Ibrahim | Medium |
| 5 | Day 20-21 | Mail Configure | Hany | Ahmed | High |
| 6 | Day 22-24 | Payment Processing | Ibrahim | Abdulrahman | High |
| 7 | Day 25-26 | Rating and Feedback | Ahmed | Hanouf | Low |
| 8 | Day 27-30 | Account MGMT | Ibrahim | Abdulrahman | Low |
| 9 | Day 31-45 | Admin MGMT | Fatimah | Hany | High |

#### Student User Stories
* As a new user, I can register an account so that I can access the platform's features. This includes collecting personal details (full name, email, password, phone number, gender, nationality, and education level). Password confirmation is required. A verification email is sent upon registration, requiring account activation before login.
* As a registered user, I can log in to the platform to access my profile and manage my registrations and preferences.
* As a user, I can manage my profile and set permissions to protect my privacy. This involves viewing and updating personal and contact information (full name, email, phone, nationality, gender, education, military status). Users can change their password securely.
* Notification preferences (email, SMS, application updates, payment confirmations) can be updated.
* As a user, I can search for available tracks based on my access.
* As a user, I can view details about each available track, including subjects and prices.
* As a user, I can modify or cancel my bookings any time I need.
* As a user, I am able to securely enter my payment information to complete a registration.
* As a user, I can receive a confirmation of my booking once the payment is processed successfully.
* As a user, I can view my upcoming and past registrations.
* As a student, I can initiate new applications for available programs, specifying degree type, academic year, and semester.
* As a student, I can upload required documents for my application (e.g., bachelor's certificate, transcript, ID).
* As a student, I can review my application details and attached documents before final submission.
* As a student, I shall be notified of application status changes via in-app notifications and email.
* As a student, I shall be able to view all my uploaded documents.
* As a student, I shall be able to upload new documents or update existing ones.
* As a student, I shall be able to delete uploaded documents.
* As a student, I shall be prompted to pay application fees once my documents are approved.
* As a student, I shall be able to pay for certificate requests.
* As a student, I shall be automatically enrolled in initial courses upon enrollment in a program.
* As a student, I shall be able to view my enrolled courses, grades (letter and numeric), and academic standing (e.g., GPA).
* As a student, I shall be notified when new grades are recorded.
* As a student, I shall be able to request various types of certificates (e.g., Transcript, Completion, Enrollment, Graduation).
* As a student, I shall be able to track the status of my certificate requests (e.g., "Pending Payment", "Processing", "Ready for Pickup").
* As a student, I shall be able to create new support tickets with a subject, category, priority, and detailed message.
* As a student, I shall be able to view my support tickets and all messages within a ticket.
* As a student, I shall be able to reply to existing tickets.
* As a student, I shall be able to close my own tickets.
* As a student, I shall receive notifications for new replies on my tickets.

#### Administrator User Stories
* As an admin, I want to be able to add, remove, or update track listings on the platform.
* As an admin, I want to be able to view and manage user registrations and their accounts.
* As an admin, I want to be able to add new tracks to my inventory on the platform so that they are available for take.
* As an admin, I want to provide detailed information about each track I list, including topics, features, and values options, to attract potential individuals.
* As an admin, I want to be able to update information about my listed tracks, such as availability and pricing, to reflect changes in my inventory.
* As an admin, I want to view a high-level overview of the portal's activity and key metrics.
* As an admin, I want to view a list of all submitted applications with details like applicant name, program, date, and status.
* As an admin, I want to search and filter applications by status or keywords.
* As an admin, I want to view detailed information and uploaded documents for a specific application in a modal window.
* As an admin, I want to approve or reject applications, which updates the application status and notifies the student.
* As an admin, I want to send a note or message to a student regarding their application, which creates a support ticket.
* As an admin, I want to utilize an AI Assistant to analyze academic transcripts.
* As an admin, I want to generate a unique university student ID for applicants who have been accepted and have paid their fees, officially enrolling them.
* As an admin, I want to view a list of all enrolled students with their generated IDs.
* As an admin, I want to manage and process student requests for official certificates.
* As an admin, I want to view a list of all certificate requests with student details and request status.
* As an admin, I want to mark a certificate as "Ready for Pickup" once it has been processed.
* As an admin, I want to create, edit, and delete news articles and announcements that are displayed on the public-facing pages of the portal.
* As an admin, I want to manage the project repository, which showcases student and faculty projects on the public website.
* As an admin, I want to configure global settings for the application, such as application fees and notification preferences.

### 3.3 Traceability Matrix

A traceability matrix is crucial for ensuring that all requirements are met and tested. It links user stories and functional requirements to design elements, code modules, and test cases. The following conceptual matrix demonstrates how traceability matrix aligns components:

| Feature/User Story ID | Description (from User Story/Feature List) | Functional Requirement ID (from SE206) | UI Component (Template/Code) | Backend Logic (File/Function) | Test Case (Derived) |
|---|---|---|---|---|---|
| ID 1 | As a user, I want to be able to register for an account on the platform. | FR1.1 | register.html | auth/routes.py/register() | TC-REG-001: Successful user registration with email verification. |
| ID 2 | As a user. I want to be able to log in to my account. | FR1.3 | login.html | auth/routes.py/login() | TC-LOGIN-001: Successful login with valid credentials. |
| ID 4 | As a user, I want to be able to view details about each available Track. | FR2.2 | programs.html | main/routes.py/program_details() | TC-VIEW-PROG-001: Verify program details are displayed correctly. |
| FR2.3 | Students shall be able to upload required documents. | FR3.2 | student/upload_document.html | main/routes.py/upload_document() | TC-DOC-UPLOAD-001: Verify successful document upload to S3. |
| FR5.2 | Administrators shall be able to generate unique student IDs. | FR5.2 | admin/enrollments.html | admin/routes.py/generate_student_id() | TC-ADMIN-ID-001: Verify unique student ID generation. |
| FR8.10 | Administrators shall be able to send general notes or messages to students. | FR8.10 | admin/applications.html | admin/routes.py/send_note_to_student() | TC-ADMIN-NOTE-001: Verify admin can send a note that creates a ticket. |
| FR11.1 | Administrators shall be able to initiate Al analysis for uploaded PDF transcripts. | FR11.1 | admin/applications.html | admin/routes.py/analyze_transcript() | TC-AI-TRANSCRIPT-001: Verify Al analysis of transcript is triggered and displayed. |

### 3.4 Product Backlog

The product backlog is a prioritized list of features and functionalities that need to be developed for the platform. Each item is associated with a story point estimation and a priority level. The following table represents key items from the product backlog:

| ID | Story | Story Point | Priority |
|---|---|---|---|
| ID_1 | As a user, I want to be able to register for an account on Cairo University Platform so that I can access its features. | 3 | 1 |
| ID 2 | As a user, I want to be able to log in to my account so that I can manage my Registration and preferences. | 3 | 1 |
| ID 3 | As a user, I want to be able to search for available Tracks based on Certificate and the cost per track. | 5 | 2 |
| ID 4 | As a user, I want to be able to view details about each available Track, including Topics, features, and prices. | 8 | 2 |
| ID 5 | As a user, I want to be able to select a Track and register it for my desired dates. | 3 | 2 |
| ID 6 | As a user, I want to be able to view my upcoming and past registration. | 5 | 3 |
| ID_7 | As a user, I want to be able to modify or edit my Profile if it is necessary. | 3 | 3 |
| ID 8 | As a user, I want to be able to securely enter my payment information to complete a registration. | 8 | 4 |
| ID 9 | As a user, I want to receive a confirmation of my booking once payment is processed successfully. | 5 | 3 |
| ID 10 | As an admin, I want to be able to add, remove, or update Track listings on the platform. | 3 | 6 |
| ID_11 | As an admin, I want to be able to view and manage user Registration and accounts. | 5 | 7 |
| ID 12 | As an admin, I want to be able to add new news, announcements and projects to the platform so that they are available for view. | 5 | 7 |
| ID 13 | As an admin, I want to provide detailed information about each Track I list, including Topics, features, and pay options. | 3 | 7 |
| ID_14 | As an admin, I want to be able to update information about my listed Track, such as availability and pricing, to reflect changes in my inventory. | 3 | 7 |

### 3.5 Project Estimation

Project estimation was performed using the Story Point Estimation Model (SPEM). This model combines three parameters to calculate the "Story Size": Story Points (SP), Implementation Level Factor (ILF), and Complexity (Com).

**Story Point (SP):** Story Points are relative measures of effort for a user story, categorized by size and weighted using the Fibonacci sequence.

| Parameter | Description | Weight |
|---|---|---|
| Very small story | 1 | |
| Small story | 2 | |
| Medium story | 3 | |
| Large story | 5 | |
| Very large story | 8 | |

**Implementation Level Factor (ILF):** ILF considers the level of understanding and experience with the components involved in a user story.

| Parameter | Description | Weight |
|---|---|---|
| Off the shelf | 1 | |
| Full experienced components | 2 | |
| Partial experienced components | 3 | |
| New components | 4 | |

**Complexity (Com):** Complexity has been determined based on the user stories in ILF.

| Parameter | Description | Weight |
|---|---|---|
| Very low | 1 | |
| Low | 2 | |
| Medium | 3 | |
| Large | 4 | |
| Very large | 5 | |

**Story Size Calculation:** The Story Size is calculated using the formula: Story Points * Implementation Level Factor * Complexity.

Here's the detailed story size estimation for each backlog item:

| ID | Story | SP | ILF | Com | Story Size |
|---|---|---|---|---|---|
| ID_1 | As a user, I want to be able to register for an account on the Faculty platform so that I can access its features. | 3 | 1 | 1 | 3 |
| ID_2 | As a user, I want to be able to log in to my account so that I can manage my Profile and preferences. | 3 | 1 | 1 | 3 |
| ID_3 | As a user, I want to be able to search for available Tracks based on my location (Online-offline) and Registration dates. | 5 | 2 | 1 | 10 |
| ID_4 | As a user, I want to be able to view details about each available Track, including its Topics, features, and price. | 8 | 2 | 2 | 32 |
| ID_5 | As a user, I want to be able to select a Track and register it for my desired dates. | 3 | 2 | 1 | 6 |
| ID_6 | As a user, I want to be able to view my upcoming and past Registration. | 5 | 1 | 2 | 10 |
| ID_7 | As a user, I want to be able to modify or edit my Profile if it is necessary. | 3 | 1 | 2 | 6 |
| ID_8 | As a user, I want to be able to securely enter my payment information to complete a Registration. | 8 | 3 | 1 | 24 |
| ID_9 | As a user, I want to receive a confirmation of my booking once payment is processed successfully. | 5 | 2 | 2 | 20 |
| ID_10 | As an admin, I want to be able to add, remove, or update Track listings on the platform. | 3 | 1 | 2 | 6 |
| ID_11 | As an admin, I want to be able to view and manage user Registration and their accounts. | 5 | 2 | 2 | 20 |
| ID 12 | As an admin, I want to be able to add new Tracks to my inventory on the platform so that they are available for take. | 5 | 1 | 2 | 10 |
| ID 13 | As an admin, I want to provide detailed information about each Track I list, including Topics, features and cost options. | 3 | 1 | 1 | 3 |
| ID_14 | As an admin, I want to be able to update information about my listed Tracks, such as availability and pricing, to reflect changes in my inventory. | 3 | 1 | 1 | 3 |
| **Total Story Size** | | | | | **156** |

**Iteration Planning:** The initial velocity for this application was set at 25 story sizes. Based on the total story size of 156, the project required 7 iterations to deliver all planned functionalities.

| Iteration Number | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Story Size | 25 | 25 | 25 | 25 | 25 | 25 | 6 |

### 3.6 Test Plan

The test plan for the Cairo University Platform aimed to ensure the system's functionality, performance, security, and usability through a combination of white box and black box testing, with a focus on traceability and leveraging log analysis for problem identification and resolution.

#### Test Objectives
* Verify that all functional and non-functional requirements are met.
* Ensure the system is secure against common vulnerabilities.
* Confirm optimal performance under various load conditions.
* Validate the user interface for intuitiveness and responsiveness.

#### Test Scope
The testing covered all modules: User Authentication & Authorization, Student Application Management, Document Management, Payment Processing, Enrollment & Student ID Generation, Course and GPA Management, Certificate Request and Fulfillment, Support Ticketing System, Content Management, Reporting and Analytics, AI Assistant Integration, and Public Access.

#### Types of Testing
1.  **White Box Testing (Structural Testing):** This focused on the internal structure and logic of the code.
    * **Unit Testing:** Individual functions and methods were tested in isolation. For example:
        * `User.set_password()` and `User.check_password()` in `app/models.py` or `models.py` would be tested to ensure correct hashing and password verification.
        * `file_management.py` (if existed) or relevant S3 upload logic within `run.py` would be tested to confirm files are uploaded correctly to AWS S3.
        * Logic for generating unique student IDs based on year, nationality, and program code within `run.py` would be thoroughly tested.
        * GPA calculation logic would be tested with various grade combinations to ensure accuracy.
    * **Integration Testing:** Different modules were tested together to ensure seamless interaction. For example, the interaction between Application submission and Document upload, and subsequent Notification creation would be tested.
    * **Code Coverage:** Tools would be used to measure the percentage of code executed by tests, aiming for high coverage to minimize untested paths.
2.  **Black Box Testing (Functional Testing):** This focused on the system's external behavior and functionality from an end-user perspective, without knowledge of the internal code. Test cases were derived directly from user stories and functional requirements.
    * **Functional Testing:**
        * **User Registration & Login:**
            * Verify successful registration with unique email, email verification, and redirection to login page.
            * Test login with valid/invalid credentials, and unverified accounts.
            * Test password reset functionality via email link.
        * **Student Application Submission:**
            * Verify multi-step application form navigation (program selection, document upload, review).
            * Confirm dynamic loading of programs based on degree type.
            * Test document upload (PDF, JPG, PNG, max 10MB) and validation.
            * Verify application status updates and notifications.
        * **Admin Application Management:**
            * Verify viewing, filtering, approving, and rejecting applications.
            * Test sending notes to students, confirming ticket creation.
            * Test AI Assistant for transcript analysis by uploading a PDF and verifying analysis results.
        * **Payment Processing:**
            * Verify fee calculation based on nationality.
            * Test application and certificate payment flows, ensuring status updates.
        * **Support Ticketing System:**
            * Verify ticket creation by students with subject, category, priority, and message.
            * Test viewing and replying to tickets by students and admins.
            * Verify ticket status updates (Open, In Progress, Closed).
    * **UI/UX Testing:** Ensured the interface was intuitive, responsive across devices, and localized for Arabic (RTL support).
    * **Performance Testing:**
        * Measured page load times (aiming for <3 seconds).
        * Assessed database query execution times (aiming for <500ms).
        * Evaluated file upload/download efficiency to/from S3 (uploads <5 seconds for <10MB files).
        * Monitored Al analysis response times (aiming for <30 seconds for standard PDFs).

#### Test Environment
* **Development:** SQLite3 database Flask's built-in server (implied by Flask framework usage ).
* **Production:** PostgreSQL database, Gunicorn with Nginx/Vercel for web serving AWS S3 for file storage, Mailtrap for emails, Google Gemini API for AI.

#### Traceability of Test Cases (Example)

| Functional Requirement | Test Case ID | Description |
|---|---|---|
| FR1.1: User registration | TC-REG-001 | Verify new users can register and receive verification email. |
| FR2.3: Document upload | TC-DOC-UPLOAD-001 | Verify students can upload documents of allowed types and sizes. |
| FR5.2: Generate Student ID | TC-ADMIN-ID-001 | Confirm unique student ID is generated and assigned. |
| FR8.6: Admin reply to tickets | TC-ADMIN-TKT-001 | Verify admin can reply to a ticket, and status updates. |
| FR11.1: AI Transcript Analysis | TC-AI-TRANSCRIPT-001 | Verify Al analysis button triggers analysis and displays results. |

#### Solution Based on Logs (White and Black Box Testing Insights)
Analysis of `logs_result.json` revealed key issues and insights into system behavior:

1.  **Missing CSRF Token Error (Critical Bug):**
    * **Log Entry:** "2025-06-25 18:37:26,884-flask_wtf.csrf - INFO - The CSRF token is missing." resulting in a HTTP 400 for POST/admin/tickets/update_status/1.
    * **Impact:** This indicates a severe security vulnerability where Flask-WTF's Cross-Site Request Forgery (CSRF) protection mechanism failed for an admin action. It means malicious requests could potentially be forged if not addressed.
    * **Solution:**
        * **White Box Solution (Code Fix):** Ensure that every form submission (especially POST requests) includes the `csrf_token` in the form data or headers. The `templates/admin/tickets.html` and `admin/routes.py` (or relevant admin routing file) should be checked to ensure the `csrf_token` is properly rendered in forms and validated on the backend. Specifically, the JavaScript logic sending the POST request for updating ticket status must include the CSRF token.
        * **Black Box Verification:** After deploying the fix, a black box test would involve manually changing a ticket status in the admin panel and monitoring network requests to confirm the CSRF token is correctly sent and the action is successful, without the 400 error.

2.  **404 Not Found Errors (Minor Configuration/Deployment Issues):**
    * **Log Entry Examples:** "GET /dist/js/bootstrap.bundle.min.js HTTP/1.1" 404 -, "GET /favicon.ico HTTP/1.1" 404 -.
    * **Impact:** These indicate that certain static assets or the favicon are not found at the requested paths. While not critical functional errors, they can affect user experience (e.g., broken icons, missing browser tab icon) and indicate deployment issues (e.g., incorrect path mapping in Vercel or missing files in the static folder).
    * **Solution:**
        * **Code/Configuration Check:** Verify the `url_for()` calls for these assets in templates (e.g., `templates/base.html` for Bootstrap JS, favicon link in HTML head). Ensure the files exist in the static directory or are correctly configured in `vercel.json` for Vercel deployments. The `vercel.json` routes/ to `api/index.py`, meaning static files might need explicit handling or serving via a different mechanism if not directly routed.
        * **Deployment Review:** Confirm that the `dist/js` folder (if used for Bootstrap) and `favicon.ico` are correctly included in the deployment package.

3.  **Performance Insights (Monitoring Focus):**
    * **Log Entry:** Various GET requests (e.g., `/admin/tickets`, `/`) show `durationMs` values ranging from 5ms to 370ms. Some `durationMs` are -1, indicating logging limitations for certain requests (e.g., in middleware or very early in the request lifecycle).
    * **Impact:** While many durations are acceptable for typical web operations, continuous monitoring is necessary. -1 durations highlight areas where more detailed performance logging could be beneficial.
    * **Solution:**
        * **Continuous Monitoring:** Implement dedicated application performance monitoring (APM) tools (e.g., Sentry, Datadog) beyond basic serverless logs to capture more granular timings and identify bottlenecks.
        * **Optimization:** Investigate functions with consistently higher `durationMs` (e.g., 370ms for `/admin/dashboard`) to optimize database queries (e.g., using `joinedload` or `selectinload` for eager loading relationships in SQLAlchemy, as seen in `app/models.py` or `models.py` database models) or computationally intensive logic.

This comprehensive test plan, coupled with continuous monitoring and log analysis, is essential for maintaining the quality, reliability, and security of the Cairo University Platform.
