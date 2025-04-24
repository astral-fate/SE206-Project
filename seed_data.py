from run import app, db
from models import Program, Course, ProgramCourse

def create_program_courses():
    with app.app_context():
        # Create programs
        programs = {
            # Software Engineering - Master's
            "master_software_eng": Program(
                name="Software Engineering",
                degree_type="Master",
                code="MSE",
                description="Advanced software engineering principles and practices"
            ),
            # Web Design - Master's
            "master_web_design": Program(
                name="Web Design",
                degree_type="Master",
                code="MWD", 
                description="Advanced web design and development techniques"
            ),
            # Add more programs as needed
        }
        
        # Add programs to database
        for program in programs.values():
            existing = Program.query.filter_by(name=program.name, degree_type=program.degree_type).first()
            if not existing:
                db.session.add(program)
        
        db.session.commit()
        
        # Create courses for Software Engineering Master