## Chapter 3: Implementation

This chapter details the implementation phase of the Cairo University Platform, outlining the methodologies, user stories, product backlog, project estimations, and a comprehensive test plan.

### 3.1 Agile Methodology

The project adopted an Agile methodology, specifically incorporating principles of iterative development and estimation based on user stories. [cite_start]This approach allowed for flexibility and continuous adaptation throughout the development lifecycle, as evidenced by the "Iteration Planning"  [cite_start]and "Story Size Estimation"  frameworks utilized. [cite_start]The project embraced incremental delivery, with a planned total of 7 iterations, each aiming to deliver 25 story sizes, demonstrating a commitment to regular progress assessment and adjustment.

### 3.2 User Stories

[cite_start]User stories served as the core of the development process, capturing functional requirements from various perspectives—students and administrators. [cite_start]These stories were derived from the initial feature list  [cite_start]and detailed use cases, guiding the development and testing efforts.

**Student User Stories:**
* [cite_start]As a new user, I can register an account so that I can access the platform's features.
    * [cite_start]This includes collecting personal details (full name, email, password, phone number, gender, nationality, and education level).
    * [cite_start]Password confirmation is required.
    * [cite_start]A verification email is sent upon registration, requiring account activation before login.
* [cite_start]As a registered user, I can log in to the platform to access my profile  [cite_start]and manage my registrations and preferences.
* [cite_start]As a user, I can manage my profile and set permissions to protect my privacy.
    * [cite_start]This involves viewing and updating personal and contact information (full name, email, phone, nationality, gender, education, military status).
    * [cite_start]Users can change their password securely.
    * [cite_start]Notification preferences (email, SMS, application updates, payment confirmations) can be updated.
* [cite_start]As a user, I can search for available tracks based on my access.
* [cite_start]As a user, I can view details about each available track, including subjects and prices.
* [cite_start]As a user, I can modify or cancel my bookings any time I need.
* [cite_start]As a user, I am able to securely enter my payment information to complete a registration.
* [cite_start]As a user, I can receive a confirmation of my booking once the payment is processed successfully.
* [cite_start]As a user, I can view my upcoming and past registrations.
* [cite_start]As a student, I can initiate new applications for available programs, specifying degree type, academic year, and semester.
* [cite_start]As a student, I can upload required documents for my application (e.g., bachelor's certificate, transcript, ID).
* [cite_start]As a student, I can review my application details and attached documents before final submission.
* [cite_start]As a student, I shall be notified of application status changes via in-app notifications and email.
* [cite_start]As a student, I shall be able to view all my uploaded documents.
* [cite_start]As a student, I shall be able to upload new documents or update existing ones.
* [cite_start]As a student, I shall be able to delete uploaded documents.
* [cite_start]As a student, I shall be prompted to pay application fees once my documents are approved.
* [cite_start]As a student, I shall be able to pay for certificate requests.
* [cite_start]As a student, I shall be automatically enrolled in initial courses upon enrollment in a program.
* [cite_start]As a student, I shall be able to view my enrolled courses, grades (letter and numeric), and academic standing (e.g., GPA).
* [cite_start]As a student, I shall be notified when new grades are recorded.
* [cite_start]As a student, I shall be able to request various types of certificates (e.g., Transcript, Completion, Enrollment, Graduation).
* [cite_start]As a student, I shall be able to track the status of my certificate requests (e.g., "Pending Payment", "Processing", "Ready for Pickup").
* [cite_start]As a student, I shall be able to create new support tickets with a subject, category, priority, and detailed message.
* [cite_start]As a student, I shall be able to view my support tickets and all messages within a ticket.
* [cite_start]As a student, I shall be able to reply to existing tickets.
* [cite_start]As a student, I shall be able to close my own tickets.
* [cite_start]As a student, I shall receive notifications for new replies on my tickets.

**Administrator User Stories:**
* [cite_start]As an admin, I want to be able to add, remove, or update track listings on the platform.
* [cite_start]As an admin, I want to be able to view and manage user registrations and their accounts.
* [cite_start]As an admin, I want to be able to add new tracks to my inventory on the platform so that they are available for take.
* [cite_start]As an admin, I want to provide detailed information about each track I list, including topics, features, and values options, to attract potential individuals.
* [cite_start]As an admin, I want to be able to update information about my listed tracks, such as availability and pricing, to reflect changes in my inventory.
* [cite_start]As an admin, I want to view a high-level overview of the portal's activity and key metrics.
* [cite_start]As an admin, I want to view a list of all submitted applications with details like applicant name, program, date, and status.
* [cite_start]As an admin, I want to search and filter applications by status or keywords.
* [cite_start]As an admin, I want to view detailed information and uploaded documents for a specific application in a modal window.
* [cite_start]As an admin, I want to approve or reject applications, which updates the application status and notifies the student.
* [cite_start]As an admin, I want to send a note or message to a student regarding their application, which creates a support ticket.
* [cite_start]As an admin, I want to utilize an AI Assistant to analyze academic transcripts.
* [cite_start]As an admin, I want to generate a unique university student ID for applicants who have been accepted and have paid their fees, officially enrolling them.
* [cite_start]As an admin, I want to view a list of all enrolled students with their generated IDs.
* [cite_start]As an admin, I want to manage and process student requests for official certificates.
* [cite_start]As an admin, I want to view a list of all certificate requests with student details and request status.
* [cite_start]As an admin, I want to mark a certificate as "Ready for Pickup" once it has been processed.
* [cite_start]As an admin, I want to create, edit, and delete news articles and announcements that are displayed on the public-facing pages of the portal.
* [cite_start]As an admin, I want to manage the project repository, which showcases student and faculty projects on the public website.
* [cite_start]As an admin, I want to configure global settings for the application, such as application fees and notification preferences.

### 3.3 Traceability Matrix

A traceability matrix is crucial for ensuring that all requirements are met and tested. It links user stories and functional requirements to design elements, code modules, and test cases. While a formal matrix is not provided, the following conceptual matrix demonstrates how it would align components:

| Feature/User Story ID | Description (from User Story/Feature List) | Functional Requirement ID (from SE206) | UI Component (Template/Code) | Backend Logic (File/Function) | Test Case (Derived) |
| :-------------------- | :----------------------------------------- | :------------------------------------- | :--------------------------- | :---------------------------- | :------------------ |
| ID_1 | As a user, I want to be able to register for an account on the platform. | [cite_start]FR1.1  | [cite_start]`register.html`  | [cite_start]`auth/routes.py`/`register()`  | TC-REG-001: Successful user registration with email verification. |
| ID_2 | As a user, I want to be able to log in to my account. | [cite_start]FR1.3  | [cite_start]`login.html`  | [cite_start]`auth/routes.py`/`login()`  | TC-LOGIN-001: Successful login with valid credentials. |
| ID_4 | As a user, I want to be able to view details about each available Track. | [cite_start]FR2.2  | [cite_start]`programs.html`  | `main/routes.py`/`program_details()` | TC-VIEW-PROG-001: Verify program details are displayed correctly. |
| FR2.3 | Students shall be able to upload required documents. | [cite_start]FR3.2  | [cite_start]`student/upload_document.html`  | `main/routes.py`/`upload_document()` | TC-DOC-UPLOAD-001: Verify successful document upload to S3. |
| FR5.2 | Administrators shall be able to generate unique student IDs. | [cite_start]FR5.2  | [cite_start]`admin/enrollments.html`  | `admin/routes.py`/`generate_student_id()` | TC-ADMIN-ID-001: Verify unique student ID generation. |
| FR8.10 | Administrators shall be able to send general notes or messages to students. | [cite_start]FR8.10  | [cite_start]`admin/applications.html`  | `admin/routes.py`/`send_note_to_student()` | TC-ADMIN-NOTE-001: Verify admin can send a note that creates a ticket. |
| FR11.1 | Administrators shall be able to initiate AI analysis for uploaded PDF transcripts. | [cite_start]FR11.1  | [cite_start]`admin/applications.html`  | `admin/routes.py`/`analyze_transcript()` | TC-AI-TRANSCRIPT-001: Verify AI analysis of transcript is triggered and displayed. |

### 3.4 Product Backlog

The product backlog is a prioritized list of features and functionalities that need to be developed for the platform. [cite_start]Each item is associated with a story point estimation and a priority level. The following table represents key items from the product backlog:

| ID | Story | Story Point | Priority |
| :----------- | :----------------------------------------------------------------------------------------------------------------- | :-------------------- | :----------------- |
| ID_1 | As a user, I want to be able to register for an account on the faculty platform so that I can access its features. | [cite_start]3  | [cite_start]1  |
| ID_2 | As a user, I want to be able to log in to my account so that I can manage my Registration and preferences. | [cite_start]3  | [cite_start]1  |
| ID_3 | As a user, I want to be able to search for available Tracks based on Certificate and the cost per track. | [cite_start]5  | [cite_start]2  |
| ID_4 | As a user, I want to be able to view details about each available Track, including Topics, features, and prices. | [cite_start]8  | [cite_start]2  |
| ID_5 | As a user, I want to be able to select a Track and register it for my desired dates. | [cite_start]3  | [cite_start]2  |
| ID_6 | As a user, I want to be able to view my upcoming and past registration. | [cite_start]5  | [cite_start]3  |
| ID_7 | As a user, I want to be able to modify or edit my Profile if it is necessary. | [cite_start]3  | [cite_start]3  |
| ID_8 | As a user, I want to be able to securely enter my payment information to complete a registration. | [cite_start]8  | [cite_start]4  |
| ID_9 | As a user, I want to receive a confirmation of my booking once payment is processed successfully. | [cite_start]5  | [cite_start]3  |
| ID_10 | As an admin, I want to be able to add, remove, or update Track listings on the platform. | [cite_start]3  | [cite_start]6  |
| ID_11 | As an admin, I want to be able to view and manage user Registration and accounts. | [cite_start]5  | [cite_start]7  |
| ID_12 | As an admin, I want to be able to add new Tracks to my inventory on the platform so that they are available for reserve. | [cite_start]5  | [cite_start]7  |
| ID_13 | As an admin, I want to provide detailed information about each Track I list, including Topics, features, and pay options. | [cite_start]3  | [cite_start]7  |
| ID_14 | As an admin, I want to be able to update information about my listed Track, such as availability and pricing, to reflect changes in my inventory. | [cite_start]3  | [cite_start]7  |

### 3.5 Project Estimation

[cite_start]Project estimation was performed using the Story Point Estimation Model (SPEM). [cite_start]This model combines three parameters to calculate the "Story Size": Story Points (SP), Implementation Level Factor (ILF), and Complexity (Com).

**Story Point (SP):**
[cite_start]Story Points are relative measures of effort for a user story, categorized by size and weighted using the Fibonacci sequence.

| Parameter | Description | Weight |
| :------------------- | :--------------------- | :---------------- |
| Very small story | [cite_start]1  | |
| Small story | [cite_start]2  | |
| Medium story | [cite_start]3  | |
| Large story | [cite_start]5  | |
| Very large story | [cite_start]8  | |

**Implementation Level Factor (ILF):**
[cite_start]ILF considers the level of understanding and experience with the components involved in a user story.

| Parameter | Description | Weight |
| :----------------------- | :--------------------------- | :---------------- |
| Off the shelf | [cite_start]1  | |
| Full experienced components | [cite_start]2  | |
| Partial experienced components | [cite_start]3  | |
| New components | [cite_start]4  | |

**Complexity (Com):**
[cite_start]Complexity has been determined based on the user stories in ILF.

| Parameter | Description | Weight |
| :------------------- | :--------------------- | :---------------- |
| Very low | [cite_start]1  | |
| Low | [cite_start]2  | |
| Medium | [cite_start]3  | |
| Large | [cite_start]4  | |
| Very large | [cite_start]5  | |

**Story Size Calculation:**
[cite_start]The Story Size is calculated using the formula: `Story Points * Implementation Level Factor * Complexity`.

[cite_start]Here's the detailed story size estimation for each backlog item:

| ID | Story | SP | ILF | Com | Story Size |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------ | :------------- | :------------- | :-------------------- |
| ID_1 | As a user, I want to be able to register for an account on the Faculty platform so that I can access its features. | [cite_start]3  | [cite_start]1  | [cite_start]1  | [cite_start]3  |
| ID_2 | As a user, I want to be able to log in to my account so that I can manage my Profile and preferences. | [cite_start]3  | [cite_start]1  | [cite_start]1  | [cite_start]3  |
| ID_3 | As a user, I want to be able to search for available Tracks based on my location (Online-offline) and Registration dates. | [cite_start]5  | [cite_start]2  | [cite_start]1  | [cite_start]10  |
| ID_4 | As a user, I want to be able to view details about each available Track, including its Topics, features, and price. | [cite_start]8  | [cite_start]2  | [cite_start]2  | [cite_start]32  |
| ID_5 | As a user, I want to be able to select a Track and register it for my desired dates. | [cite_start]3  | [cite_start]2  | [cite_start]1  | [cite_start]6  |
| ID_6 | As a user, I want to be able to view my upcoming and past Registration. | [cite_start]5  | [cite_start]1  | [cite_start]2  | [cite_start]10  |
| ID_7 | As a user, I want to be able to modify or edit my Profile if it is necessary. | [cite_start]3  | [cite_start]1  | [cite_start]2  | [cite_start]6  |
| ID_8 | As a user, I want to be able to securely enter my payment information to complete a Registration. | [cite_start]8  | [cite_start]3  | [cite_start]1  | [cite_start]24  |
| ID_9 | As a user, I want to receive a confirmation of my booking once payment is processed successfully. | [cite_start]5  | [cite_start]2  | [cite_start]2  | [cite_start]20  |
| ID_10 | As an admin, I want to be able to add, remove, or update Track listings on the platform. | [cite_start]3  | [cite_start]1  | [cite_start]2  | [cite_start]6  |
| ID_11 | As an admin, I want to be able to view and manage user Registration and their accounts. | [cite_start]5  | [cite_start]2  | [cite_start]2  | [cite_start]20  |
| ID_12 | As an admin, I want to be able to add new Tracks to my inventory on the platform so that they are available for take. | [cite_start]5  | [cite_start]1  | [cite_start]2  | [cite_start]10  |
| ID_13 | As an admin, I want to provide detailed information about each Track I list, including Topics, features and cost options. | [cite_start]3  | [cite_start]1  | [cite_start]1  | [cite_start]3  |
| ID_14 | As an admin, I want to be able to update information about my listed Tracks, such as availability and pricing, to reflect changes in my inventory. | [cite_start]3  | [cite_start]1  | [cite_start]1  | [cite_start]3  |
| **Total Story Size** | | | | | [cite_start]**156**  |

**Iteration Planning:**
The initial velocity for this application was set at 25 story sizes. [cite_start]Based on the total story size of 156, the project required 7 iterations to deliver all planned functionalities.

| Iteration Number | [cite_start]1  | [cite_start]2  | [cite_start]3  | [cite_start]4  | [cite_start]5  | [cite_start]6  | [cite_start]7  |
| :--------------------------- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Story Size | [cite_start]25  | [cite_start]25  | [cite_start]25  | [cite_start]25  | [cite_start]25  | [cite_start]25  | [cite_start]6  |

### 3.6 Test Plan

The test plan for the Cairo University Platform aimed to ensure the system's functionality, performance, security, and usability through a combination of white box and black box testing, with a focus on traceability and leveraging log analysis for problem identification and resolution.

**Test Objectives:**
* [cite_start]Verify that all functional  [cite_start]and non-functional requirements  are met.
* [cite_start]Ensure the system is secure against common vulnerabilities.
* [cite_start]Confirm optimal performance under various load conditions.
* [cite_start]Validate the user interface for intuitiveness and responsiveness.

**Test Scope:**
[cite_start]The testing covered all modules: User Authentication & Authorization, Student Application Management, Document Management, Payment Processing, Enrollment & Student ID Generation, Course and GPA Management, Certificate Request and Fulfillment, Support Ticketing System, Content Management, Reporting and Analytics, AI Assistant Integration, and Public Access.

**Types of Testing:**

1.  **White Box Testing (Structural Testing):**
    This focused on the internal structure and logic of the code.
    * **Unit Testing:** Individual functions and methods were tested in isolation. For example:
        * `User.set_password()` and `User.check_password()` in `app/models.py` or `models.py` (depending on the actual location) would be tested to ensure correct hashing and password verification.
        * `file_management.py` (if existed) or relevant S3 upload logic within `run.py`  would be tested to confirm files are uploaded correctly to AWS S3.
        * Logic for generating unique student IDs based on year, nationality, and program code within `run.py`  would be thoroughly tested.
        * GPA calculation logic would be tested with various grade combinations to ensure accuracy.
    * **Integration Testing:** Different modules were tested together to ensure seamless interaction. For example, the interaction between `Application` submission  and `Document` upload , and subsequent `Notification` creation  would be tested.
    * **Code Coverage:** Tools would be used to measure the percentage of code executed by tests, aiming for high coverage to minimize untested paths.

2.  **Black Box Testing (Functional Testing):**
    This focused on the system's external behavior and functionality from an end-user perspective, without knowledge of the internal code. Test cases were derived directly from user stories and functional requirements.
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
    * **UI/UX Testing:** Ensured the interface was intuitive , responsive across devices , and localized for Arabic (RTL support).
    * **Performance Testing:**
        * Measured page load times (aiming for <3 seconds).
        * Assessed database query execution times (aiming for <500ms).
        * Evaluated file upload/download efficiency to/from S3 (uploads <5 seconds for <10MB files).
        * Monitored AI analysis response times (aiming for <30 seconds for standard PDFs).

**Test Environment:**
* [cite_start]**Development:** SQLite3 database [cite: 77][cite_start], Flask's built-in server (implied by Flask framework usage ).
* [cite_start]**Production:** PostgreSQL database [cite: 78, 85][cite_start], Gunicorn with Nginx/Vercel for web serving [cite: 76, 80][cite_start], AWS S3 for file storage [cite: 86][cite_start], Mailtrap for emails [cite: 88][cite_start], Google Gemini API for AI.

**Traceability of Test Cases (Example):**

| Functional Requirement | Test Case ID | Description |
| :------------------------------------- | :----------- | :---------- |
| [cite_start]FR1.1: User registration  | TC-REG-001 | Verify new user can register and receive verification email. |
| [cite_start]FR2.3: Document upload  | TC-DOC-UPLOAD-001 | Verify students can upload documents of allowed types and sizes. |
| [cite_start]FR5.2: Generate Student ID  | TC-ADMIN-ID-001 | Confirm unique student ID is generated and assigned. |
| [cite_start]FR8.6: Admin reply to tickets  | TC-ADMIN-TKT-001 | Verify admin can reply to a ticket, and status updates. |
| [cite_start]FR11.1: AI Transcript Analysis  | TC-AI-TRANSCRIPT-001 | Verify AI analysis button triggers analysis and displays results. |

**Solution Based on Logs (White and Black Box Testing Insights):**

Analysis of `logs_result (20).json` revealed key issues and insights into system behavior:

1.  **Missing CSRF Token Error (Critical Bug):**
    * **Log Entry:** `"2025-06-25 18:37:26,884 - flask_wtf.csrf - INFO - The CSRF token is missing."` resulting in a `HTTP 400` for `POST /admin/tickets/update_status/1`.
    * [cite_start]**Impact:** This indicates a severe security vulnerability where `Flask-WTF`'s Cross-Site Request Forgery (CSRF) protection mechanism failed for an admin action. It means malicious requests could potentially be forged if not addressed.
    * **Solution:**
        * **White Box Solution (Code Fix):** Ensure that every form submission (especially POST requests) includes the `csrf_token` in the form data or headers. The `templates/admin/tickets.html` and `admin/routes.py` (or relevant admin routing file) should be checked to ensure the `csrf_token` is properly rendered in forms and validated on the backend. Specifically, the JavaScript logic sending the `POST` request for updating ticket status must include the CSRF token.
        * **Black Box Verification:** After deploying the fix, a black box test would involve manually changing a ticket status in the admin panel and monitoring network requests to confirm the CSRF token is correctly sent and the action is successful, without the 400 error.

2.  **404 Not Found Errors (Minor Configuration/Deployment Issues):**
    * **Log Entry Examples:**
        * `"GET /dist/js/bootstrap.bundle.min.js HTTP/1.1" 404 -`
        * `"GET /favicon.ico HTTP/1.1" 404 -`
    * **Impact:** These indicate that certain static assets or the favicon are not found at the requested paths. While not critical functional errors, they can affect user experience (e.g., broken icons, missing browser tab icon) and indicate deployment issues (e.g., incorrect path mapping in Vercel or missing files in the static folder).
    * **Solution:**
        * **Code/Configuration Check:** Verify the `url_for()` calls for these assets in templates (e.g., `templates/base.html` for Bootstrap JS, favicon link in HTML head). Ensure the files exist in the `static` directory or are correctly configured in `vercel.json` for Vercel deployments. The `vercel.json` routes `/(.*)` to `api/index.py`, meaning static files might need explicit handling or serving via a different mechanism if not directly routed.
        * **Deployment Review:** Confirm that the `dist/js` folder (if used for Bootstrap) and `favicon.ico` are correctly included in the deployment package.

3.  **Performance Insights (Monitoring Focus):**
    * **Log Entries:** Various `GET` requests (e.g., `/admin/tickets`, `/`) show `durationMs` values ranging from 5ms to 370ms. Some `durationMs` are `-1`, indicating logging limitations for certain requests (e.g., in `middleware` or very early in the request lifecycle).
    * **Impact:** While many durations are acceptable for typical web operations, continuous monitoring is necessary. `-1` durations highlight areas where more detailed performance logging could be beneficial.
    * **Solution:**
        * **Continuous Monitoring:** Implement dedicated application performance monitoring (APM) tools (e.g., Sentry, Datadog) beyond basic serverless logs to capture more granular timings and identify bottlenecks.
        * **Optimization:** Investigate functions with consistently higher `durationMs` (e.g., 370ms for `/admin/dashboard`) to optimize database queries (e.g., using `joinedload` or `selectinload` for eager loading relationships in SQLAlchemy, as seen in `app/models.py` or `models.py` database models) or computationally intensive logic.

This comprehensive test plan, coupled with continuous monitoring and log analysis, is essential for maintaining the quality, reliability, and security of the Cairo University Platform.
