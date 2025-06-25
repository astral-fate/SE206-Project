# Use Case Descriptions for Cairo University Platform

This document provides detailed use case descriptions for the Cairo University Platform, following the template provided in `image_49b456.png`. The use cases are categorized into student-facing and admin-facing functionalities, based on the analysis of the provided project files and the `cu-platform (1).png` use case diagram.

---

### 1. User Login

| Use Case Name | User Login |
| :------------ | :--------- |
| **Brief Description** | Allows users (students and administrators) to log in to the system using their registered credentials. |
| **Actors** | Registered User (Student, Admin) |
| **Preconditions** | User is not logged in. The user's account must be verified (for students). |
| **Triggers** | User selects 'Login' option. User attempts to access a protected page. |
| **Basic Flow** | 1. User selects 'Login' option.<br>2. System displays the login form.<br>3. User enters their email and password.<br>4. User submits the login form.<br>5. System validates the user's credentials.<br>6. If validation is successful, the system logs the user in and directs them to their respective dashboard (student or admin). |
| **Alternative Flow** | **A1: Invalid Credentials**<br>1. If the entered email or password is incorrect, the system displays an "Invalid email or password" error message.<br>**A2: Account Not Verified (for students)**<br>1. If the user is a student and their account is not verified, the system displays a message prompting them to verify their account.<br>**A3: Forgot Password**<br>1. User selects 'Forgot Password?' option.<br>2. System guides the user through the password recovery process (see "Forgot Password / Reset Password" Use Case). |
| **Postconditions** | The user is successfully logged in, and their authentication token is active. The user is redirected to their appropriate dashboard. |

---

### 2. Sign Up (Register)

| Use Case Name | Sign Up (Register) |
| :------------ | :----------------- |
| **Brief Description** | Allows new users to create an account on the university platform. |
| **Actors** | Prospective Student |
| **Preconditions** | User does not have an existing account. |
| **Triggers** | User selects 'Register' or 'Sign Up' option. |
| **Basic Flow** | 1. User selects 'Register' option.<br>2. System displays the registration form.<br>3. User enters required personal details (full name, email, password, confirm password, phone, nationality, gender, education, and military status if applicable).<br>4. User submits the registration form.<br>5. System validates the input data (e.g., password match, email uniqueness).<br>6. If validation is successful, the system creates a new unverified user account.<br>7. The system sends a verification email to the user's registered email address.<br>8. The system redirects the user to the login page and displays a success message, prompting them to verify their account. |
| **Alternative Flow** | **A1: Email Already Registered**<br>1. If the email provided is already registered, the system displays an "Email already registered" error message.<br>**A2: Passwords Do Not Match**<br>1. If the password and confirm password fields do not match, the system displays a "Passwords do not match" error message.<br>**A3: Email Sending Failure**<br>1. If the verification email fails to send due to a system error, the system displays a warning message instructing the user to contact support, but the account is still created. |
| **Postconditions** | A new user account is created and saved in the database, marked as unverified. A verification email is sent to the user. |

---

### 3. Forgot Password / Reset Password

| Use Case Name | Forgot Password / Reset Password |
| :------------ | :------------------------------- |
| **Brief Description** | Allows a user to reset their password if they have forgotten it by sending a reset link to their registered email address. |
| **Actors** | Registered User (Student, Admin) |
| **Preconditions** | User is not logged in. The user's account must be verified (for students) to receive a reset email. |
| **Triggers** | User clicks 'Forgot Password?' link on the login page. |
| **Basic Flow** | **Part 1: Request Reset Link**<br>1. User clicks 'Forgot Password?' on the login page.<br>2. System displays the "Forgot Password" request form.<br>3. User enters their registered email address and submits the form.<br>4. System checks if the email is registered and the account is verified.<br>5. If valid, the system generates a time-sensitive password reset token and sends an email containing a reset link to the user's email address.<br>6. System redirects the user to the login page and displays a generic confirmation message.<br><br>**Part 2: Reset Password**<br>1. User receives the email and clicks on the password reset link.<br>2. System validates the reset token (validity and expiration).<br>3. If the token is valid, the system displays the "Reset Password" form.<br>4. User enters a new password and confirms it.<br>5. User submits the form.<br>6. System updates the user's password in the database.<br>7. System redirects the user to the login page and displays a success message. |
| **Alternative Flow** | **A1: Email Not Registered/Not Verified**<br>1. If the email is not found or the account is not verified, the system still displays a generic success message to prevent user enumeration.<br>**A2: Invalid or Expired Token**<br>1. If the reset token is invalid or expired, the system displays an error message and redirects the user to the "Forgot Password" request page.<br>**A3: Passwords Do Not Match**<br>1. If the new password and confirmation do not match, the system displays an error and allows the user to re-enter. |
| **Postconditions** | If successful, the user's password is updated in the system, and they can now log in with the new password. |

---

### 4. Manage Account (Update Personal Info)

| Use Case Name | Manage Account (Update Personal Info) |
| :------------ | :------------------------------------ |
| **Brief Description** | Allows a logged-in student to view and update their personal and contact information. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. |
| **Triggers** | User navigates to 'Profile' or 'Settings' page. |
| **Basic Flow** | 1. User navigates to the 'Profile' or 'Settings' page.<br>2. System displays the user's current personal information (e.g., full name, email, phone, nationality, gender, education, military status).<br>3. User modifies one or more fields.<br>4. User clicks 'Save Changes'.<br>5. System validates the updated information.<br>6. System updates the user's profile in the database.<br>7. System displays a success message. |
| **Alternative Flow** | **A1: Invalid Input**<br>1. If any input is invalid (e.g., malformed email), the system displays an error message.<br>**A2: Change Password**<br>1. User navigates to "Change Password" section (within settings).<br>2. User enters current password, new password, and confirms new password.<br>3. System validates current password and new password match.<br>4. System updates the password and displays a success message.<br>**A3: Update Notification Preferences**<br>1. User modifies notification preferences (email, SMS, application updates, payment confirmations).<br>2. User clicks 'Save Preferences'.<br>3. System updates preferences and displays a success message. |
| **Postconditions** | The user's personal information is updated in the database. |

---

### 5. Submit New Application

| Use Case Name | Submit New Application |
| :------------ | :--------------------- |
| **Brief Description** | Allows a student to apply for a new academic program offered by the university. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. User has not submitted an application for the selected program for the current academic year/semester. |
| **Triggers** | User clicks 'Submit New Application' button on the applications dashboard or main page. |
| **Basic Flow** | 1. User clicks 'Submit New Application'.<br>2. System displays a multi-step application form starting with program selection.<br>3. **Step 1: Choose Program**<br>    a. User selects degree type, academic year, and semester.<br>    b. System dynamically loads and displays available programs based on selections.<br>    c. User selects a program, and system displays program details (e.g., courses, total credits).<br>    d. User clicks 'Next'.<br>4. **Step 2: Upload Documents**<br>    a. System lists required documents based on program and user nationality.<br>    b. User uploads each required document (PDF, JPG, PNG, max 10MB).<br>    c. User clicks 'Next'.<br>5. **Step 3: Review and Submit**<br>    a. System displays a summary of the selected program and uploaded documents.<br>    b. User reviews the information and clicks 'Submit Final Application'.<br>6. System creates a new application record in the database with 'Pending Review' status.<br>7. System saves all uploaded documents to S3 and records their paths in the database.<br>8. System creates a new notification for the student and sends a confirmation email.<br>9. System redirects the user to the 'My Applications' page and displays a success message. |
| **Alternative Flow** | **A1: Missing Program Fields**<br>1. If required program fields are not selected, the system displays an error.<br>**A2: Missing/Invalid Documents**<br>1. If any required documents are missing, have invalid file types, or exceed size limits, the system displays an error and prevents submission.<br>**A3: Document Upload Failure (S3)**<br>1. If a document fails to upload to S3, the entire transaction is rolled back, and an error message is displayed.<br>**A4: Database Error**<br>1. If a database error occurs during application or document creation, the transaction is rolled back, and an error message is displayed.<br>**A5: Email Confirmation Failure**<br>1. If the confirmation email fails to send, the system logs the error but the application submission process continues to completion. |
| **Postconditions** | A new application is created with 'Pending Review' status. All submitted documents are stored in S3 and linked to the application. A notification and email confirmation are sent to the student. |

---

### 6. Upload Documents

| Use Case Name | Upload Documents |
| :------------ | :--------------- |
| **Brief Description** | Allows a student to upload new documents or update existing ones, optionally linking them to an application. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. S3 service is configured and available. |
| **Triggers** | User clicks 'Upload Document' button on the dashboard or documents page. User clicks 'Update' next to a document on the 'My Documents' page. |
| **Basic Flow** | 1. User initiates document upload/update.<br>2. System displays the document upload form.<br>3. If it's a new upload:<br>    a. User selects document type and optionally links it to an existing application.<br>4. If it's an update:<br>    a. The form is pre-filled with the existing document's details, and document type/application link fields are disabled.<br>5. User selects a file to upload (PDF, JPG, PNG, max 10MB).<br>6. User submits the form.<br>7. System validates the file type and size.<br>8. System uploads the file to S3.<br>9. If it's a new upload, a new document record is created in the database.<br>10. If it's an update, the existing document record is updated with the new file path, and the old file is deleted from S3.<br>11. The document status is set to 'تم الرفع' (Uploaded).<br>12. System redirects to 'My Documents' page and displays a success message. |
| **Alternative Flow** | **A1: Missing File/Invalid Input**<br>1. If no file is selected or document type is missing (for new uploads), or file type/size is invalid, the system displays an error message.<br>**A2: S3 Service Unavailable**<br>1. If the S3 service is not configured, the system redirects to 'My Documents' and displays an error.<br>**A3: S3 Upload/Delete Failure**<br>1. If uploading the new file or deleting the old file from S3 fails, the system displays an error message.<br>**A4: Database Error**<br>1. If a database error occurs during document creation or update, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | The document is uploaded to S3 and its record is created/updated in the database. The previous version of the document (if updating) is removed from S3. |

---

### 7. Complete Payment (for Application)

| Use Case Name | Complete Payment (for Application) |
| :------------ | :------------------------------- |
| **Brief Description** | Allows a student to pay the application fees after their documents have been approved. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. The student has an application with 'مقبول مبدئياً' (Documents Approved) status and 'بانتظار الدفع' (Pending Payment) payment status. |
| **Triggers** | User clicks 'Pay Now' button from the dashboard or application details page. |
| **Basic Flow** | 1. User clicks 'Pay Now' for a specific application.<br>2. System displays the payment confirmation page, showing application details and the fee amount (determined by nationality).<br>3. User clicks 'Confirm Payment'.<br>4. System processes the payment (simulated).<br>5. System creates a new payment record in the database.<br>6. System updates the application's payment status to 'مدفوع' (Paid).<br>7. System sends a notification to all administrators about the completed payment.<br>8. System redirects the user to 'My Applications' and displays a success message. |
| **Alternative Flow** | **A1: Already Paid**<br>1. If the application's payment status is not 'بانتظار الدفع', the system redirects the user back to 'My Applications' with an informative message.<br>**A2: Database Error**<br>1. If a database error occurs during payment processing or status update, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | A payment record is created. The application's payment status is updated to 'مدفوع'. Administrators are notified of the payment. |

---

### 8. Request Certificate

| Use Case Name | Request Certificate |
| :------------ | :------------------ |
| **Brief Description** | Allows a student to request various types of official certificates from the university. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. |
| **Triggers** | User clicks 'Request Certificate' button on the certificates page. |
| **Basic Flow** | 1. User clicks 'Request Certificate'.<br>2. System displays the certificate request form.<br>3. User selects the certificate type, specifies the purpose, and enters the number of copies.<br>4. As the user selects a certificate type, the system dynamically displays information about it (e.g., processing time, fee, format).<br>5. User submits the request.<br>6. System creates a new certificate request record with 'بانتظار الدفع' (Pending Payment) status.<br>7. System redirects the user to 'My Certificates' page and displays a success message, prompting for payment.<br>8. **Extend: Complete Payment (for Certificate)**: User proceeds to payment for the certificate. |
| **Alternative Flow** | **A1: Invalid Input**<br>1. If required fields are not filled or values are invalid (e.g., copies < 1), the system displays an error.<br>**A2: Database Error**<br>1. If a database error occurs during certificate request creation, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | A new certificate request is created with 'بانتظار الدفع' status. The user is prompted to complete the payment for the certificate. |

---

### 9. View Enrolled Courses / View Graded Courses

| Use Case Name | View Enrolled Courses / View Graded Courses |
| :------------ | :---------------------------------------- |
| **Brief Description** | Allows a student to view their currently enrolled courses, including their status, and any grades received for completed courses. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. Student must have an 'مسجل' (Enrolled) application. |
| **Triggers** | User clicks 'Courses' link in the student dashboard. |
| **Basic Flow** | 1. User clicks 'Courses' link.<br>2. System identifies the student's active enrolled program and automatically enrolls them in the appropriate courses for the current academic year/semester if not already enrolled.<br>3. System retrieves all enrolled courses for the student, including course codes, titles, credits, semester, status, letter grade, and numerical grade.<br>4. System displays the list of enrolled courses in a table. |
| **Alternative Flow** | **A1: No Enrolled Program**<br>1. If the student does not have an 'مسجل' (Enrolled) application, the system indicates that no courses are available and skips auto-enrollment.<br>**A2: Auto-Enrollment Error**<br>1. If an error occurs during automatic enrollment, the system displays an error message, but still attempts to display existing enrollments.<br>**A3: No Courses Found**<br>1. If no courses are found for auto-enrollment in the selected program or no existing enrollments, the system displays a message indicating no courses are available. |
| **Postconditions** | The student views a list of their enrolled courses. New enrollments may have been automatically added if applicable. |

---

### 10. Submit Support Ticket

| Use Case Name | Submit Support Ticket |
| :------------ | :-------------------- |
| **Brief Description** | Allows a student to create a new support ticket to communicate issues or inquiries to the administration. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. |
| **Triggers** | User clicks 'New Ticket' button on the support page. |
| **Basic Flow** | 1. User clicks 'New Ticket'.<br>2. System displays the new ticket form.<br>3. User enters the subject, selects a category, sets priority, types the message, and optionally links it to an application.<br>4. User submits the form.<br>5. System generates a unique ticket ID.<br>6. System creates a new ticket record with 'Open' status and adds the initial message.<br>7. System redirects the user to 'Support Tickets' page and displays a success message. |
| **Alternative Flow** | **A1: Missing Fields**<br>1. If subject or message fields are empty, the system displays an "Error: Please fill out all required fields." message.<br>**A2: Database Error**<br>1. If a database error occurs during ticket creation, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | A new support ticket is created with an 'Open' status and the student's initial message. |

---

### 11. View Admin Messages

| Use Case Name | View Admin Messages |
| :------------ | :------------------ |
| **Brief Description** | Allows a student to view and reply to support tickets, including messages from administrators. |
| **Actors** | Registered Student |
| **Preconditions** | User is logged in as a student. Student has existing support tickets. |
| **Triggers** | User clicks on a specific ticket from the support tickets list. |
| **Basic Flow** | 1. User clicks on a ticket from the 'Support Tickets' list.<br>2. System displays the detailed conversation view for that ticket, showing all messages exchanged, including those from 'Admin'.<br>3. If the ticket is not 'Closed', user can type a reply in the message box.<br>4. User clicks 'Send'.<br>5. System adds the new message to the ticket conversation.<br>6. If the ticket was 'Closed', its status changes to 'In Progress'.<br>7. System sends a notification to administrators about the new reply.<br>8. The chat interface updates to show the new message and scrolls to the bottom. |
| **Alternative Flow** | **A1: Ticket Closed**<br>1. If the ticket is 'Closed', the reply form is hidden, and an option to 'Reopen Ticket' might be presented.<br>2. If the user reopens the ticket, its status changes to 'In Progress', and the reply form becomes available again.<br>**A2: Empty Message**<br>1. If the user tries to send an empty message, the system displays an error.<br>**A3: Unauthorized Access**<br>1. If a user attempts to view a ticket that does not belong to them, the system displays an 'Access Denied' message. |
| **Postconditions** | The student views the full conversation history. New messages from the student are added to the ticket. Ticket status may change from 'Closed' to 'In Progress' upon reply. Administrators receive a notification about the new reply. |

---

### 12. Manage Applications (Admin)

| Use Case Name | Manage Applications (Admin) |
| :------------ | :-------------------------- |
| **Brief Description** | Allows administrators to view, accept, or reject student applications. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. |
| **Triggers** | Administrator navigates to 'Applications' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'Applications'.<br>2. System displays a list of all applications, with options to view, accept, or reject.<br>3. Admin can filter applications by status or search by keywords.<br>4. Admin clicks 'View' for a specific application.<br>5. System opens a modal displaying application details and uploaded documents.<br>6. Admin can view individual documents within the modal.<br>7. Admin clicks 'قبول' (Approve) or 'رفض' (Reject) for applications with 'قيد المراجعة' status.<br>8. System updates the application status to 'مقبول مبدئياً' (Documents Approved) or 'المستندات مرفوضة' (Documents Rejected).<br>9. System sends a notification and email to the student about the status update.<br>10. The application list refreshes to reflect the change. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Invalid Action**<br>1. If an invalid action is attempted on an application, the system displays an error.<br>**A3: View Document Failure**<br>1. If a document cannot be previewed (e.g., unsupported format), the system shows a fallback message and offers a download option.<br>**A4: Database Error**<br>1. If a database error occurs during status update, the transaction is rolled back, and an error is displayed. |
| **Postconditions** | Application status is updated. Student is notified of the status change via in-app notification and email. |

---

### 13. Send Note (Admin)

| Use Case Name | Send Note (Admin) |
| :------------ | :---------------- |
| **Brief Description** | Allows an administrator to send a direct message (note) to an applicant regarding their application, which creates a support ticket on the student's side. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. |
| **Triggers** | Administrator clicks 'Note' button next to an application. |
| **Basic Flow** | 1. Admin clicks 'Note' for a specific application.<br>2. System opens a modal with a form for subject and message.<br>3. Admin enters a subject (pre-filled with application ID) and types the message.<br>4. Admin clicks 'Send Note'.<br>5. System creates a new support ticket with 'Open' status associated with the student and adds the admin's message as the first entry.<br>6. System sends an in-app notification and an email to the student informing them of the new message.<br>7. System closes the modal and displays a success message. |
| **Alternative Flow** | **A1: Missing Fields**<br>1. If subject or message fields are empty, the system displays an error message.<br>**A2: Database Error**<br>1. If a database error occurs during ticket/message creation, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | A new support ticket is created for the student with the admin's message. The student receives an in-app notification and an email about the new message. |

---

### 14. Analyze Uploaded Documents (Admin)

| Use Case Name | Analyze Uploaded Documents (Admin) |
| :------------ | :--------------------------------- |
| **Brief Description** | Allows an administrator to trigger an AI analysis of a student's uploaded academic transcript (PDF) to extract key information. |
| **Actors** | Admin, AI Service (Gemini) |
| **Preconditions** | User is logged in as an administrator. The uploaded document is a PDF academic transcript. Gemini API and S3 are configured. |
| **Triggers** | Administrator clicks 'AI Assistant - Analyze Academic Transcript' button in the document viewer modal. |
| **Basic Flow** | 1. Admin opens the document viewer for an academic transcript PDF.<br>2. Admin clicks 'AI Assistant - Analyze Academic Transcript'.<br>3. System displays a loading spinner in a new modal.<br>4. System downloads the PDF transcript from S3.<br>5. System encodes the PDF content to Base64.<br>6. System sends the Base64 encoded PDF along with a prompt to the Gemini AI service.<br>7. AI Service processes the request and returns the analysis text.<br>8. System displays the AI-generated analysis text in the modal. |
| **Alternative Flow** | **A1: AI Service Not Configured**<br>1. If Gemini API key is missing, the button is disabled or an error message is displayed when clicked.<br>**A2: S3 Service Not Configured/Unavailable**<br>1. If S3 is not configured or an error occurs during PDF download from S3, the system displays an error message.<br>**A3: AI Analysis Failure**<br>1. If the AI service returns an error or an empty response, the system displays an appropriate error message in the modal.<br>**A4: Non-PDF Document**<br>1. The AI analysis button is only visible for documents identified as transcripts (based on name) and is expected to be a PDF. If the file is not a PDF, an error would occur during processing. |
| **Postconditions** | The administrator receives an AI-generated summary or analysis of the academic transcript. |

---

### 15. Manage Certificates (Admin)

| Use Case Name | Manage Certificates (Admin) |
| :------------ | :-------------------------- |
| **Brief Description** | Allows administrators to view and process student certificate requests, marking them as ready for pickup. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. Students have submitted certificate requests. |
| **Triggers** | Administrator navigates to 'Certificates' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'Certificates'.<br>2. System displays a list of all certificate requests, including certificate ID, student name, type, request date, and current status.<br>3. Admin can filter certificates by status or search by keywords.<br>4. For certificates with 'قيد التجهيز' (Processing) status, Admin clicks 'تحديد كجاهزة' (Mark as Ready).<br>5. System updates the certificate status to 'جاهزة للاستلام' (Ready for Pickup).<br>6. System sends a notification and an email to the student informing them that their certificate is ready for pickup.<br>7. The certificate list refreshes to reflect the change. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Certificate Not Ready for Processing**<br>1. The 'Mark as Ready' button is disabled for certificates not in 'بانتظار الدفع' (Pending Payment) or 'قيد التجهيز' (Processing) status.<br>**A3: Database Error**<br>1. If a database error occurs during status update, the transaction is rolled back, and an error is displayed. |
| **Postconditions** | Certificate status is updated to 'جاهزة للاستلام'. Student is notified via in-app notification and email to pick up the certificate. |

---

### 16. Grade Courses (Admin)

| Use Case Name | Grade Courses (Admin) |
| :------------ | :-------------------- |
| **Brief Description** | Allows an administrator to view a student's enrolled courses and assign or update their numerical and letter grades. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. The student is enrolled in courses. |
| **Triggers** | Administrator clicks 'View Courses' for a specific student from the 'Students' list. |
| **Basic Flow** | 1. Admin navigates to a specific student's courses page.<br>2. System displays the student's personal and academic information, including a list of all courses they are associated with (enrolled or not).<br>3. For enrolled courses, Admin clicks 'تحديث الدرجة' (Update Grade).<br>4. System opens a modal displaying the course title and a field for numerical grade (0-100).<br>5. As Admin types the numerical grade, the system automatically displays the corresponding letter grade.<br>6. Admin clicks 'حفظ الدرجة' (Save Grade).<27>7. System updates the course enrollment record with the numerical grade, letter grade, GPA value, and sets the status to 'مكتمل' (Completed) or 'راسب' (Failed).<br>8. System sends a notification and an email to the student about their new grade.<br>9. The course list refreshes to show the updated grade. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Invalid Grade Input**<br>1. If the entered grade is not a valid number (0-100), the system displays an error message.<br>**A3: No Student ID**<br>1. If the student does not have a university ID assigned, the system displays a warning and redirects back to the 'Students' page.<br>**A4: Database Error**<br>1. If a database error occurs during grade update, the transaction is rolled back, and an error is displayed. |
| **Postconditions** | The student's course enrollment record is updated with the new grade and status. The student receives an in-app notification and email about the grade. |

---

### 17. Generate Student ID (Admin)

| Use Case Name | Generate Student ID (Admin) |
| :------------ | :-------------------------- |
| **Brief Description** | Allows an administrator to generate a unique university ID for a student once their application is fully approved and paid. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. An application has 'مقبول مبدئياً' (Documents Approved) status and 'مدفوع' (Paid) payment status, and no student ID has been generated yet. |
| **Triggers** | Administrator navigates to 'Enrollments' from the admin dashboard. Admin clicks 'إنشاء رقم جامعي' (Generate Student ID). |
| **Basic Flow** | 1. Admin navigates to 'Enrollments'.<br>2. System displays a list of applications pending student ID generation.<br>3. Admin clicks 'إنشاء رقم جامعي' for a specific application.<br>4. System opens a modal for confirmation and allows an optional custom prefix for the ID.<br>5. Admin clicks 'إنشاء رقم جامعي' within the modal.<br>6. System generates a unique student ID based on year, nationality, program, and a sequential number.<br>7. System creates a new `StudentID` record in the database.<br>8. System updates the application's status to 'مسجل' (Enrolled).<br>9. System sends a notification and an email to the student informing them of their new student ID.<br>10. The application is removed from the 'Pending Student IDs' list and appears in 'Enrolled Students'. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Application Not Eligible**<br>1. If the application is not in the correct status (Approved and Paid), the 'Generate Student ID' button is not available.<br>**A3: Database Error**<br>1. If a database error occurs during ID generation or status update, the transaction is rolled back, and an error is displayed. |
| **Postconditions** | A unique student ID is generated and assigned to the student. The application status is updated to 'مسجل'. The student receives an in-app notification and email with their new ID. |

---

### 18. Manage Support Tickets (Admin)

| Use Case Name | Manage Support Tickets (Admin) |
| :------------ | :----------------------------- |
| **Brief Description** | Allows administrators to view, filter, update the status of, and reply to student support tickets. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. Students have submitted support tickets. |
| **Triggers** | Administrator navigates to 'Support Tickets' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'Support Tickets'.<br>2. System displays a list of all tickets, including ticket ID, student, subject, creation date, last update, and status.<br>3. Admin can filter tickets by status ('Open', 'In Progress', 'Closed') or search by keywords.<br>4. Admin views ticket analytics (counts of open, in progress, closed tickets, common issues).<br>5. Admin clicks 'عرض' (View) for a specific ticket or changes its status directly using the dropdown.<br>6. **If View is clicked:**<br>    a. System displays the detailed conversation view for the ticket.<br>    b. Admin can change the ticket status using a dropdown in the detail view.<br>    c. Admin types a reply message and clicks 'Send'.<br>    d. System adds the reply to the conversation, and if the ticket was 'Open', changes its status to 'In Progress'.<br>    e. System sends a notification and email to the student about the new reply. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Invalid Status Change**<br>1. If an invalid status is selected, the system displays an error.<br>**A3: Empty Reply Message**<br>1. If an admin attempts to send an empty reply, the system displays an error message.<br>**A4: Database Error**<br>1. If a database error occurs during ticket update or reply, the transaction is rolled back, and an error is displayed. |
| **Postconditions** | Ticket status is updated. New messages are added to the ticket conversation. Students are notified of replies or status changes. |

---

### 19. Manage News and Announcements (Admin)

| Use Case Name | Manage News and Announcements (Admin) |
| :------------ | :------------------------------------ |
| **Brief Description** | Allows administrators to create, edit, and delete news articles and announcements displayed on the public-facing website. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. S3 service is configured for image uploads. |
| **Triggers** | Administrator navigates to 'News & Announcements' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'News & Announcements'.<br>2. System displays a table of existing news items and announcements.<br>3. **To Add New:**<br>    a. Admin clicks 'Add New'.<br>    b. System displays the 'Add News/Announcement' form.<br>    c. Admin fills in title, content, type (news/announcement), publication date, optional image, and sets active/featured status.<br>    d. Admin clicks 'Publish'.<br>    e. System uploads image to S3 (if provided) and saves the new item to the database.<br>    f. System redirects to the news list and displays a success message.<br>4. **To Edit Existing:**<br>    a. Admin clicks 'Edit' for a news item.<br>    b. System displays the 'Edit News/Announcement' form, pre-filled with current data.<br>    c. Admin modifies fields and optionally uploads a new image.<br>    d. Admin clicks 'Update Changes'.<br>    e. System updates the item in the database, replacing the image in S3 if a new one was uploaded.<br>    f. System redirects to the news list and displays a success message.<br>5. **To Delete:**<br>    a. Admin clicks 'Delete' for a news item.<br>    b. System prompts for confirmation.<br>    c. If confirmed, system deletes the item from the database and its image from S3.<br>    d. System removes the item from the list and displays a success message. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: S3 Service Unavailable/Image Upload Fail**<br>1. If S3 is not configured or an image upload fails, an error message is displayed.<br>**A3: Invalid Input/Validation Fail**<br>1. If required fields are missing, date format is incorrect, or file type/size is invalid, the system displays an error.<br>**A4: Database Error**<br>1. If a database error occurs during add, edit, or delete, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | News items or announcements are created, updated, or deleted, affecting what is displayed on the public website. Images associated with news items are managed in S3. |

---

### 20. Manage Projects (Admin)

| Use Case Name | Manage Projects (Admin) |
| :------------ | :---------------------- |
| **Brief Description** | Allows administrators to add, edit, toggle status, and delete academic projects displayed in the project repository. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. S3 service is configured for image uploads. |
| **Triggers** | Administrator navigates to 'Projects' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'Projects'.<br>2. System displays a table of existing projects.<br>3. **To Add New:**<br>    a. Admin clicks 'Add New Project'.<br>    b. System displays the 'Add New Project' form.<br>    c. Admin fills in project details (title, description, category, URL), uploads an optional image, and sets active/popular status.<br>    d. Admin clicks 'Save Project'.<br>    e. System uploads image to S3 (if provided) and saves the new project to the database.<br>    f. System redirects to the projects list and displays a success message.<br>4. **To Edit Existing:**<br>    a. Admin clicks 'Edit' for a project.<br>    b. System displays the 'Edit Project' form, pre-filled with current data.<br>    c. Admin modifies fields and optionally uploads a new image.<br>    d. Admin clicks 'Save Changes'.<br>    e. System updates the project in the database, replacing the image in S3 if a new one was uploaded.<br>    f. System redirects to the projects list and displays a success message.<br>5. **To Toggle Status (Active/Popular):**<br>    a. Admin toggles the 'Active' or 'Popular' switch.<br>    b. System updates the `is_active` or `is_popular` flag in the database.<br>    c. System displays a success message.<br>6. **To Delete:**<br>    a. Admin clicks 'Delete' for a project.<br>    b. System prompts for confirmation.<br>    c. If confirmed, system deletes the project from the database and its image from S3.<br>    d. System removes the project from the list and displays a success message. |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: S3 Service Unavailable/Image Upload Fail**<br>1. If S3 is not configured or an image upload fails, an error message is displayed.<br>**A3: Invalid Input/Validation Fail**<br>1. If required fields are missing, or file type/size is invalid, the system displays an error.<br>**A4: Database Error**<br>1. If a database error occurs during add, edit, or delete, the transaction is rolled back, and an error message is displayed. |
| **Postconditions** | Projects are created, updated, or deleted, affecting what is displayed in the project repository. Project images are managed in S3. Project visibility and "featured" status are controlled. |

---

### 21. System Settings (Admin)

| Use Case Name | System Settings (Admin) |
| :------------ | :---------------------- |
| **Brief Description** | Allows administrators to configure various system-wide settings, including fee amounts and notification preferences. |
| **Actors** | Admin |
| **Preconditions** | User is logged in as an administrator. |
| **Triggers** | Administrator navigates to 'Settings' from the admin dashboard. |
| **Basic Flow** | 1. Admin navigates to 'Settings'.<br>2. System displays current fee settings (local, international, certificate) and notification preferences (email, SMS, push).<br>3. Admin modifies fee amounts or toggles notification preferences.<br>4. Admin clicks 'Save Fee Settings' or 'Save Notification Settings'.<br>5. System updates the corresponding settings. (Note: In the provided code, this is client-side simulation, in a real app it would update the database).<br>6. System displays a success message.<br>7. Admin can also initiate a database backup or clear all read notifications (client-side simulation). |
| **Alternative Flow** | **A1: Unauthorized Access**<br>1. If a non-admin attempts to access this page, they are redirected to the student dashboard with an error.<br>**A2: Invalid Fee Input**<br>1. If non-numeric values are entered for fees, the system would prevent submission (client-side validation).<br>**A3: Database Error**<br>1. In a real application, if a database error occurs during settings update, the transaction would roll back, and an error message would be displayed. (This is not explicitly handled in the provided `admin_settings` route in `run.py` but is a general best practice). |
| **Postconditions** | System settings (fees, notification preferences) are updated. |
