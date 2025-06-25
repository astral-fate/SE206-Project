# Database Design - Data Dictionary

## User Table (user)

| Column Name     | Data Type          | Description                         | Constraints                                   |
| :-------------- | :----------------- | :---------------------------------- | :-------------------------------------------- |
| id              | INTEGER            | Unique identifier for the user      | Primary Key                                   |
| email           | VARCHAR(120)       | User's email address                | UNIQUE, NOT NULL                              |
| password_hash   | VARCHAR(256)       | Hashed password                     | NOT NULL                                      |
| full_name       | VARCHAR(120)       | Full name of the user               | NOT NULL                                      |
| role            | VARCHAR(20)        | User's role (e.g., student, admin)  | DEFAULT 'student'                             |
| created_at      | DATETIME           | Timestamp when the user was created | DEFAULT current UTC timestamp                 |
| phone           | VARCHAR(20)        | User's phone number                 |                                               |
| nationality     | VARCHAR(50)        | User's nationality                  |                                               |
| education       | VARCHAR(100)       | User's education details            |                                               |
| gender          | VARCHAR(10)        | User's gender                       |                                               |
| military_status | VARCHAR(20)        | User's military status              |                                               |
| is_verified     | BOOLEAN            | Indicates if the user is verified   | DEFAULT FALSE, NOT NULL                       |

## Program Table (programs)

| Column Name     | Data Type    | Description                                 | Constraints                        |
| :-------------- | :----------- | :------------------------------------------ | :--------------------------------- |
| id              | INTEGER      | Unique identifier for the program           | Primary Key                        |
| name            | VARCHAR(150) | Name of the program                         | NOT NULL                           |
| degree_type     | VARCHAR(50)  | Type of degree offered by the program       | NOT NULL                           |
| description     | TEXT         | Description of the program                  |                                    |
| arabic_name     | VARCHAR(200) | Arabic name of the program                  |                                    |
| arabic_description | TEXT         | Arabic description of the program           |                                    |
| type            | VARCHAR(50)  | Category or type of the program             | DEFAULT 'Professional'             |
| is_active       | BOOLEAN      | Indicates if the program is currently active | DEFAULT TRUE, NOT NULL             |

## Course Table (courses)

| Column Name | Data Type    | Description                           | Constraints                |
| :---------- | :----------- | :------------------------------------ | :------------------------- |
| id          | INTEGER      | Unique identifier for the course      | Primary Key                |
| code        | VARCHAR(20)  | Unique course code                    | UNIQUE, NOT NULL           |
| title       | VARCHAR(200) | Title of the course                   | NOT NULL                   |
| credits     | INTEGER      | Number of credits for the course      | DEFAULT 3, NOT NULL        |
| description | TEXT         | Description of the course             |                            |
| is_active   | BOOLEAN      | Indicates if the course is currently active | DEFAULT TRUE               |

## ProgramCourse Table (program_courses) - Association Table

| Column Name | Data Type | Description                              | Constraints                             |
| :---------- | :-------- | :--------------------------------------- | :-------------------------------------- |
| program_id  | INTEGER   | Foreign Key referencing the program table | Foreign Key to programs.id, Primary Key |
| course_id   | INTEGER   | Foreign Key referencing the course table  | Foreign Key to courses.id, Primary Key  |
| semester    | INTEGER   | Semester in which the course is offered  | NOT NULL                                |

## Application Table (application)

| Column Name   | Data Type          | Description                                    | Constraints                                   |
| :------------ | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id            | INTEGER            | Unique identifier for the application          | Primary Key                                   |
| app_id        | VARCHAR(50)        | Unique application identifier                  | UNIQUE, NOT NULL                              |
| user_id       | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |
| program_id    | INTEGER            | Foreign Key referencing the programs table     | Foreign Key to programs.id                    |
| program       | VARCHAR(200)       | Name of the program applied for                | NOT NULL                                      |
| status        | VARCHAR(50)        | Current status of the application              | DEFAULT 'Pending Review'                      |
| payment_status | VARCHAR(50)        | Payment status of the application              | DEFAULT 'Pending Payment'                     |
| date_submitted | DATETIME           | Timestamp when the application was submitted   | DEFAULT current UTC timestamp                 |
| academic_year | VARCHAR(20)        | Academic year of the application               |                                               |
| semester      | VARCHAR(10)        | Semester of the application                    |                                               |
| program_type  | VARCHAR(50)        | Type of program applied for                    |                                               |

## Document Table (document)

| Column Name    | Data Type          | Description                                    | Constraints                                   |
| :------------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id             | INTEGER            | Unique identifier for the document             | Primary Key                                   |
| user_id        | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |
| application_id | INTEGER            | Foreign Key referencing the application table  | Foreign Key to application.id                 |
| name           | VARCHAR(100)       | Name of the document                           | NOT NULL                                      |
| file_path      | VARCHAR(255)       | Path to the document file                      | NOT NULL                                      |
| status         | VARCHAR(50)        | Status of the document (e.g., Uploaded, Verified) | DEFAULT 'Uploaded'                            |
| uploaded_at    | DATETIME           | Timestamp when the document was uploaded       | DEFAULT current UTC timestamp                 |

## CourseEnrollment Table (course_enrollments)

| Column Name      | Data Type          | Description                                    | Constraints                                   |
| :--------------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id               | INTEGER            | Unique identifier for the enrollment           | Primary Key                                   |
| student_id       | INTEGER            | Foreign Key referencing the user (student) table | Foreign Key to user.id, NOT NULL              |
| course_id        | INTEGER            | Foreign Key referencing the courses table      | Foreign Key to courses.id, NOT NULL           |
| program_id       | INTEGER            | Foreign Key referencing the programs table     | Foreign Key to programs.id                    |
| grade            | VARCHAR(5)         | Letter grade received                          |                                               |
| grade_numeric    | FLOAT              | Numeric grade received                         |                                               |
| gpa_value        | FLOAT              | GPA value for the course                       |                                               |
| status           | VARCHAR(20)        | Enrollment status (e.g., Enrolled, Completed)  | DEFAULT 'Enrolled'                            |
| enrollment_date  | DATETIME           | Date of enrollment                             | DEFAULT current UTC timestamp                 |
| academic_year    | VARCHAR(20)        | Academic year of enrollment                    |                                               |
| semester         | VARCHAR(50)        | Semester of enrollment                         |                                               |

## StudentID Table (student_id)

| Column Name    | Data Type          | Description                                    | Constraints                                   |
| :------------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id             | INTEGER            | Unique identifier for the student ID record    | Primary Key                                   |
| student_id     | VARCHAR(50)        | Unique student ID number                       | UNIQUE, NOT NULL                              |
| application_id | INTEGER            | Foreign Key referencing the application table  | Foreign Key to application.id, UNIQUE, NOT NULL |
| issue_date     | DATETIME           | Date when the student ID was issued            | DEFAULT current UTC timestamp                 |
| created_at     | DATETIME           | Timestamp when the record was created          | DEFAULT current UTC timestamp                 |

## Certificate Table (certificates)

| Column Name   | Data Type          | Description                                    | Constraints                                   |
| :------------ | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id            | INTEGER            | Unique identifier for the certificate          | Primary Key                                   |
| cert_id       | VARCHAR(50)        | Unique certificate ID                          | UNIQUE                                        |
| user_id       | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |
| type          | VARCHAR(100)       | Type of certificate (e.g., Graduation, Transcript) | NOT NULL                                      |
| purpose       | TEXT               | Purpose of the certificate request             |                                               |
| copies        | INTEGER            | Number of copies requested                     | DEFAULT 1                                     |
| status        | VARCHAR(50)        | Status of the certificate request              | DEFAULT 'Pending Payment'                     |
| request_date  | DATETIME           | Date of certificate request                    | DEFAULT current UTC timestamp                 |

## Ticket Table (ticket)

| Column Name | Data Type          | Description                                | Constraints                               |
| :---------- | :----------------- | :----------------------------------------- | :---------------------------------------- |
| id          | INTEGER            | Unique identifier for the ticket           | Primary Key                               |
| ticket_id   | VARCHAR(20)        | Unique ticket identifier                   | UNIQUE, NOT NULL                          |
| user_id     | INTEGER            | Foreign Key referencing the user table     | Foreign Key to user.id, NOT NULL          |
| subject     | VARCHAR(100)       | Subject of the ticket                      | NOT NULL                                  |
| status      | VARCHAR(20)        | Status of the ticket (e.g., Open, Closed)  | DEFAULT 'Open'                            |
| created_at  | DATETIME           | Timestamp when the ticket was created      | DEFAULT current UTC timestamp             |

## TicketMessage Table (ticket_message)

| Column Name | Data Type          | Description                                | Constraints                               |
| :---------- | :----------------- | :----------------------------------------- | :---------------------------------------- |
| id          | INTEGER            | Unique identifier for the ticket message   | Primary Key                               |
| ticket_id   | INTEGER            | Foreign Key referencing the ticket table   | Foreign Key to ticket.id, NOT NULL        |
| sender      | VARCHAR(20)        | Sender of the message (e.g., User, Admin)  | NOT NULL                                  |
| message     | TEXT               | Content of the message                     | NOT NULL                                  |
| created_at  | DATETIME           | Timestamp when the message was created     | DEFAULT current UTC timestamp             |

## Notification Table (notification)

| Column Name | Data Type          | Description                                    | Constraints                                   |
| :---------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id          | INTEGER            | Unique identifier for the notification         | Primary Key                                   |
| user_id     | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |
| message     | VARCHAR(255)       | Content of the notification                    | NOT NULL                                      |
| read        | BOOLEAN            | Indicates if the notification has been read    | DEFAULT FALSE                                 |
| created_at  | DATETIME           | Timestamp when the notification was created    | DEFAULT current UTC timestamp                 |
| url         | VARCHAR(255)       | URL associated with the notification (if any)  |                                               |

## Payment Table (payment)

| Column Name    | Data Type          | Description                                    | Constraints                                   |
| :------------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id             | INTEGER            | Unique identifier for the payment              | Primary Key                                   |
| user_id        | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |
| application_id | INTEGER            | Foreign Key referencing the application table  | Foreign Key to application.id                 |
| certificate_id | INTEGER            | Foreign Key referencing the certificates table | Foreign Key to certificates.id                |
| amount         | FLOAT              | Amount of the payment                          | NOT NULL                                      |
| payment_method | VARCHAR(50)        | Method of payment                              | NOT NULL                                      |
| status         | VARCHAR(20)        | Status of the payment (e.g., Completed, Failed) | DEFAULT 'Completed'                           |
| transaction_id | VARCHAR(100)       | Unique transaction identifier                  |                                               |
| payment_date   | DATETIME           | Date of the payment                            | DEFAULT current UTC timestamp                 |

## Project Table (project)

| Column Name | Data Type          | Description                                    | Constraints                                   |
| :---------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id          | INTEGER            | Unique identifier for the project              | Primary Key                                   |
| title       | VARCHAR(200)       | Title of the project                           | NOT NULL                                      |
| description | TEXT               | Description of the project                     |                                               |
| category    | VARCHAR(100)       | Category of the project                        |                                               |
| url         | VARCHAR(200)       | URL for the project (if any)                   |                                               |
| image_path  | VARCHAR(200)       | Path to the project image                      |                                               |
| is_popular  | BOOLEAN            | Indicates if the project is marked as popular  | DEFAULT FALSE                                 |
| is_active   | BOOLEAN            | Indicates if the project is currently active   | DEFAULT TRUE                                  |
| created_at  | DATETIME           | Timestamp when the project was created         | DEFAULT current UTC timestamp                 |
| user_id     | INTEGER            | Foreign Key referencing the user table         | Foreign Key to user.id, NOT NULL              |

## News Table (news)

| Column Name | Data Type          | Description                                    | Constraints                                   |
| :---------- | :----------------- | :--------------------------------------------- | :-------------------------------------------- |
| id          | INTEGER            | Unique identifier for the news item            | Primary Key                                   |
| title       | VARCHAR(200)       | Title of the news item                         | NOT NULL                                      |
| description | TEXT               | Full content/description of the news item      | NOT NULL                                      |
| type        | VARCHAR(20)        | Type of news (e.g., Announcement, Event)       | NOT NULL                                      |
| date        | DATETIME           | Date of the news item                          | NOT NULL, DEFAULT current UTC timestamp       |
| image_path  | VARCHAR(200)       | Path to the news image                         |                                               |
| is_active   | BOOLEAN            | Indicates if the news item is currently active | DEFAULT TRUE                                  |
| created_at  | DATETIME           | Timestamp when the news item was created       | DEFAULT current UTC timestamp                 |
| updated_at  | DATETIME           | Timestamp when the news item was last updated  | DEFAULT current UTC timestamp, on update current UTC timestamp |
