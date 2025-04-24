from flask_migrate import Migrate
from run import app, db
from models import CourseEnrollment

migrate = Migrate(app, db)

def upgrade_db():
    """Add gpa_value column to course_enrollments table"""
    print("Starting database migration to add gpa_value column...")
    with app.app_context():
        # Use db.engine to directly execute SQL
        db.engine.execute('ALTER TABLE course_enrollments ADD COLUMN gpa_value FLOAT')
        print("Migration completed successfully!")

if __name__ == '__main__':
    upgrade_db()
