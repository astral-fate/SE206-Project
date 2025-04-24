from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Configure app with proper paths
app.config.update(
    SECRET_KEY='your-secret-key-goes-here',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///cu_project.db',
    UPLOAD_FOLDER='static/uploads'
)

# Initialize database
db = SQLAlchemy(app)

with app.app_context():
    # Execute the SQL statement to add the column
    try:
        print("Adding gpa_value column to course_enrollments table...")
        db.session.execute(text("ALTER TABLE course_enrollments ADD COLUMN gpa_value FLOAT"))
        db.session.commit()
        print("Database updated successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating database: {str(e)}")
        
    # Verify the column was added
    try:
        result = db.session.execute(text("PRAGMA table_info(course_enrollments)")).fetchall()
        columns = [row[1] for row in result]
        if 'gpa_value' in columns:
            print("Verification successful: gpa_value column exists.")
        else:
            print("Verification failed: gpa_value column not found.")
    except Exception as e:
        print(f"Error verifying column: {str(e)}")
