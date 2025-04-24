from models import db, Program, Course, ProgramCourse
from flask import Flask
from datetime import datetime, UTC
import os

def add_course_if_not_exists(code, title, credits, semester, is_active=True):
    course = Course.query.filter_by(code=code).first()
    if not course:
        course = Course(
            code=code,
            title=title,
            credits=credits,
            semester=semester,
            description=f"Course covering {title}",
            is_active=is_active
        )
        db.session.add(course)
        print(f"Added course: {code} - {title} (Semester {semester})")
        db.session.flush()
    return course

def populate_statistics_programs():
    """Add all missing statistical programs to the database"""
    statistics_programs = [
        {
            "name": "Data Science", "degree_type": "Diploma", "type": "Professional",
            "arabic_name": "علوم البيانات", "arabic_description": "دبلوم مهني في علوم البيانات",
            "courses": {
                1: [
                    {"code": "DS101", "title": "Introduction to Data Science", "credits": 3},
                    {"code": "DS102", "title": "Programming for Data Science (Python)", "credits": 3},
                    {"code": "DS103", "title": "Data Wrangling and Visualization", "credits": 3},
                    {"code": "DS104", "title": "Statistical Inference for Data Science", "credits": 3},
                    {"code": "DS105", "title": "Database Systems for Data Science", "credits": 3}
                ],
                2: [
                    {"code": "DS201", "title": "Machine Learning Fundamentals", "credits": 3},
                    {"code": "DS202", "title": "Big Data Technologies", "credits": 3},
                    {"code": "DS203", "title": "Data Mining Techniques", "credits": 3},
                    {"code": "DS204", "title": "Data Science Ethics and Privacy", "credits": 3},
                    {"code": "DS205", "title": "Data Science Project", "credits": 3}
                ]
            }
        },
        {
            "name": "Applied Statistics", "degree_type": "Master", "type": "Professional",
            "arabic_name": "الإحصاء التطبيقي", "arabic_description": "ماجستير مهني في الإحصاء التطبيقي",
            "courses": {
                1: [
                    {"code": "AS501", "title": "Advanced Statistical Theory", "credits": 3},
                    {"code": "AS502", "title": "Regression Analysis", "credits": 3},
                    {"code": "AS503", "title": "Multivariate Analysis", "credits": 3},
                ],
                2: [
                    {"code": "AS506", "title": "Time Series Analysis", "credits": 3},
                    {"code": "AS507", "title": "Computational Statistics", "credits": 3},
                    {"code": "AS508", "title": "Master's Project", "credits": 6},
                ]
            }
        },
    ]

    for program_info in statistics_programs:
        existing_program = Program.query.filter_by(
            degree_type=program_info['degree_type'],
            name=program_info['name']
        ).first()

        program = None
        if not existing_program:
            program = Program(
                name=program_info['name'],
                degree_type=program_info['degree_type'],
                type=program_info.get('type', 'Professional'),
                arabic_name=program_info.get('arabic_name'),
                arabic_description=program_info.get('arabic_description'),
                description=f"{program_info['degree_type']} in {program_info['name']}"
            )
            db.session.add(program)
            db.session.flush()
            print(f"Added Program: {program.name} ({program.degree_type}) - Type: {program.type}")
        else:
            program = existing_program
            if program.type != program_info.get('type', 'Professional'):
                program.type = program_info.get('type', 'Professional')
                print(f"Updating type for existing program: {program.name} ({program.degree_type})")
                db.session.flush()
            print(f"Program {program.name} ({program.degree_type}) already exists.")

        if program and program.id:
            for semester, courses_list in program_info['courses'].items():
                for course_data in courses_list:
                    course = add_course_if_not_exists(
                        course_data['code'],
                        course_data['title'],
                        course_data['credits'],
                        semester
                    )

                    if course and course.id:
                        existing_assoc = ProgramCourse.query.filter_by(
                            program_id=program.id,
                            course_id=course.id
                        ).first()
                        if not existing_assoc:
                            program_course = ProgramCourse(
                                program_id=program.id,
                                course_id=course.id,
                                semester=semester
                            )
                            db.session.add(program_course)
                            print(f"  Associated course {course.code} with program {program.name} (Semester {semester})")

    try:
        db.session.commit()
        print("Statistics programs and courses population/update complete.")
    except Exception as e:
        db.session.rollback()
        print(f"Error during statistics program population: {str(e)}")
        traceback.print_exc()

def populate_additional_programs():
    """Add other non-statistics programs from the text file"""
    print("Adding additional programs from the text file...")
    
    programs = [
        {"degree_type": "Diploma", "name": "Project Management", 
         "arabic_name": "إدارة المشروعات",
         "description": "A diploma program focusing on project management principles and applications."},
        {"degree_type": "Master", "name": "Project Management", 
         "arabic_name": "إدارة المشروعات",
         "description": "A master's program focusing on advanced project management."},
        {"degree_type": "PhD", "name": "Project Management", 
         "arabic_name": "إدارة المشروعات",
         "description": "A doctoral program focused on project management research."},
        
        {"degree_type": "Diploma", "name": "Operations Research and Decision Support", 
         "arabic_name": "بحوث العمليات ودعم القرار",
         "description": "A diploma program focusing on operations research and decision support."},
        {"degree_type": "Master", "name": "Operations Research and Decision Support", 
         "arabic_name": "بحوث العمليات ودعم القرار",
         "description": "A master's program focusing on advanced operations research."},
        {"degree_type": "PhD", "name": "Operations Research and Decision Support", 
         "arabic_name": "بحوث العمليات ودعم القرار",
         "description": "A doctoral program focused on operations research."},
        
        {"degree_type": "Diploma", "name": "Supply Chain and Operations Management", 
         "arabic_name": "سلسلة الإمداد وإدارة العمليات",
         "description": "A diploma program focusing on supply chain and operations management."},
        
        {"degree_type": "Diploma", "name": "Web Design", 
         "arabic_name": "تصميم المواقع",
         "description": "A diploma program focusing on web design and development."},
        
        {"degree_type": "Diploma", "name": "Software Engineering", 
         "arabic_name": "هندسة البرمجيات",
         "description": "A diploma program focusing on software engineering principles."},
        {"degree_type": "Master", "name": "Software Engineering", 
         "arabic_name": "هندسة البرمجيات",
         "description": "A master's program focusing on advanced software engineering."},
        {"degree_type": "PhD", "name": "Software Engineering", 
         "arabic_name": "هندسة البرمجيات",
         "description": "A doctoral program focused on software engineering research."},
        
        {"degree_type": "Diploma", "name": "Modern Management for Human Resources", 
         "arabic_name": "الإدارة الحديثة للموارد البشرية",
         "description": "A diploma program focusing on human resource management."},
        {"degree_type": "Master", "name": "Modern Management for Human Resources", 
         "arabic_name": "الإدارة الحديثة للموارد البشرية",
         "description": "A master's program focusing on advanced HR management."},
        {"degree_type": "PhD", "name": "Modern Management for Human Resources", 
         "arabic_name": "الإدارة الحديثة للموارد البشرية",
         "description": "A doctoral program focused on HR management research."},
        
        {"degree_type": "Diploma", "name": "Risk and Crisis Management", 
         "arabic_name": "إدارة المخاطر والأزمات",
         "description": "A diploma program focusing on risk and crisis management."},
        {"degree_type": "Master", "name": "Risk and Crisis Management", 
         "arabic_name": "إدارة المخاطر والأزمات",
         "description": "A master's program focusing on advanced risk management."},
        {"degree_type": "PhD", "name": "Risk and Crisis Management", 
         "arabic_name": "إدارة المخاطر والأزمات",
         "description": "A doctoral program focused on risk management research."}
    ]
    
    for program_info in programs:
        existing_program = Program.query.filter_by(
            degree_type=program_info['degree_type'],
            name=program_info['name']
        ).first()
        
        if existing_program:
            print(f"Program already exists: {program_info['degree_type']} in {program_info['name']}")
            if not existing_program.arabic_name:
                existing_program.arabic_name = program_info['arabic_name']
                print(f"Updated Arabic name for: {program_info['name']}")
        else:
            program = Program(
                name=program_info['name'],
                degree_type=program_info['degree_type'],
                description=program_info['description'],
                arabic_name=program_info['arabic_name']
            )
            db.session.add(program)
            print(f"Added program: {program_info['degree_type']} in {program_info['name']}")
    
    db.session.commit()
    print("Completed adding additional programs!")
    
def validate_all_programs_have_arabic_names():
    """Ensure all programs have Arabic names"""
    print("Validating Arabic names for all programs...")
    
    programs = Program.query.all()
    updated_count = 0
    
    default_translations = {
        "Statistics": "الإحصاء",
        "Applied Statistics": "الإحصاء التطبيقي",
        "Biostatistics": "الإحصاء الحيوي",
        "Population Studies": "الدراسات السكانية",
        "Computer Science": "علوم الحاسب",
        "Statistical Computing": "الحسابات الإحصائية",
        "Project Management": "إدارة المشروعات",
        "Operations Research": "بحوث العمليات",
        "Software Engineering": "هندسة البرمجيات",
        "Web Design": "تصميم المواقع",
        "Supply Chain Management": "إدارة سلسلة التوريد"
    }
    
    for program in programs:
        if not program.arabic_name:
            if program.name in default_translations:
                program.arabic_name = default_translations[program.name]
                print(f"Added missing Arabic name for {program.name}: {program.arabic_name}")
                updated_count += 1
            else:
                program.arabic_name = f"برنامج {program.name}"
                print(f"Added placeholder Arabic name for {program.name}: {program.arabic_name}")
                updated_count += 1
    
    if updated_count > 0:
        db.session.commit()
        print(f"Updated Arabic names for {updated_count} programs.")
    else:
        print("All programs already have Arabic names.")

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cu_project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.init_app(app)
        populate_statistics_programs()
        populate_additional_programs()
        validate_all_programs_have_arabic_names()
