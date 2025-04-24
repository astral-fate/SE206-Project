import sqlite3
import os

def migrate_db():
    """Add gpa_value column to course_enrollments table"""
    print("Starting database migration to add gpa_value column...")
    
    # Path to database - use absolute path for reliability
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cu_project.db')
    
    # Connect directly to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists first
        cursor.execute("PRAGMA table_info(course_enrollments)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'gpa_value' not in columns:
            print("Adding gpa_value column to course_enrollments table...")
            # Add the column
            cursor.execute('ALTER TABLE course_enrollments ADD COLUMN gpa_value FLOAT')
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("Column gpa_value already exists, no migration needed.")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(course_enrollments)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'gpa_value' in columns:
            print("Verification successful: gpa_value column exists.")
        else:
            print("Verification failed: gpa_value column not found.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {str(e)}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    migrate_db()
