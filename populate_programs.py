# Create a file called populate_programs.py

from run import app, db
from models import Program, Course, ProgramCourse
from sqlalchemy import text

def populate_programs_and_courses():
    with app.app_context():
        # Project Management
        pm_diploma = Program(name='Project Management', degree_type='Diploma', 
                           description='Program for project management fundamentals')
        pm_master = Program(name='Project Management', degree_type='Master',
                          description='Advanced project management concepts and techniques')
        pm_phd = Program(name='Project Management', degree_type='PhD',
                       description='Doctoral studies in project management')
        
        # Software Engineering
        se_diploma = Program(name='Software Engineering', degree_type='Diploma',
                           description='Program for software engineering fundamentals')
        se_master = Program(name='Software Engineering', degree_type='Master',
                          description='Advanced software engineering concepts and methodologies')
        se_phd = Program(name='Software Engineering', degree_type='PhD',
                       description='Doctoral studies in software engineering')
        
        # Add all programs
        db.session.add_all([pm_diploma, pm_master, pm_phd, se_diploma, se_master, se_phd])
        db.session.commit()
        
        # Project Management Diploma Courses
        pm_diploma_courses = [
            Course(code='PM101', title='Fundamentals of Project Management', semester=1, credits=3),
            Course(code='PM102', title='Data Analysis', semester=1, credits=3),
            Course(code='PM103', title='Planning and Scheduling', semester=1, credits=3),
            Course(code='PM104', title='Organization Structure and Communication', semester=1, credits=3),
            Course(code='PM105', title='Decision Making', semester=1, credits=3),
            Course(code='PM201', title='Budgeting and Cost', semester=2, credits=3),
            Course(code='PM202', title='Crises and Risk Management', semester=2, credits=3),
            Course(code='PM203', title='Project Control', semester=2, credits=3),
            Course(code='PM204', title='Total Quality Management', semester=2, credits=3),
            Course(code='PM205', title='Project', semester=2, credits=6)
        ]
        
        # Add courses to database first and commit them to get IDs
        for course in pm_diploma_courses:
            db.session.add(course)
        db.session.commit()
        
        # Now associate courses with program
        for course in pm_diploma_courses:
            # Make sure course.id is not None before executing the statement
            if course.id is not None:
                stmt = text(
                    "INSERT INTO program_courses (program_id, course_id, semester) VALUES (:program_id, :course_id, :semester)"
                )
                db.session.execute(stmt, {"program_id": pm_diploma.id, "course_id": course.id, "semester": course.semester})
            else:
                print(f"Warning: Course {course.code} does not have an ID")
        
        # Software Engineering Master Courses
        se_master_courses = [
            Course(code='SE501', title='Principles and Methodologies of Scientific Research', semester=1, credits=3),
            Course(code='SE502', title='Software Quality Assurance', semester=1, credits=3),
            Course(code='SE503', title='Advanced Topics in Database', semester=1, credits=3),
            Course(code='SE504', title='Advanced Topics in Information Systems', semester=2, credits=3),
            Course(code='SE505', title='Information Security', semester=2, credits=3),
            Course(code='SE506', title='Advanced Agile Software Development', semester=2, credits=3),
            Course(code='SE507', title='Project', semester=2, credits=6)
        ]
        
        # Add courses to database first and commit
        for course in se_master_courses:
            db.session.add(course)
        db.session.commit()
        
        # Associate with program after courses have IDs
        for course in se_master_courses:
            if course.id is not None:
                stmt = text(
                    "INSERT INTO program_courses (program_id, course_id, semester) VALUES (:program_id, :course_id, :semester)"
                )
                db.session.execute(stmt, {"program_id": se_master.id, "course_id": course.id, "semester": course.semester})
        
        db.session.commit()
        
        print("Programs and courses have been populated!")

if __name__ == '__main__':
    populate_programs_and_courses()