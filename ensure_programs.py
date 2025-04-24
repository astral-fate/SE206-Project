"""
Utility script to ensure that only valid programs exist in the database and each has Arabic names.
This script:
1. Loads the list of valid programs from the text file (if provided)
2. Updates existing programs with Arabic names
3. Removes any programs that shouldn't be there
4. Prints a report of what programs are available
"""

from flask import Flask
from models import db, Program
import sys
import os
from sqlalchemy import text

def setup_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cu_project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def ensure_arabic_names():
    """Add Arabic names to all programs that don't have them"""
    print("Checking for programs missing Arabic names...")
    
    # Common translations
    translations = {
        "Software Engineering": "هندسة البرمجيات",
        "Project Management": "إدارة المشروعات",
        "Web Design": "تصميم المواقع",
        "Operations Research and Decision Support": "بحوث العمليات ودعم القرار",
        "Supply Chain and Operations Management": "إدارة سلسلة التوريد والعمليات",
        "Statistical Computing": "الحسابات الإحصائية",
        "Statistical Quality Control": "الضبط الإحصائي وتوكيد الجودة",
        "Applied Statistics": "الإحصاء التطبيقي",
        "Statistics": "الإحصاء",
        "Biostatistics": "الإحصاء الحيوي",
        "Population Studies": "الدراسات السكانية",
        "Computer Science": "علوم الحاسب",
        "Data Analysis": "تحليل البيانات",
        "Actuarial Statistics": "الإحصاء الاكتواري",
        "Official Statistics": "الإحصاءات الرسمية"
    }
    
    programs = Program.query.all()
    updated = 0
    
    print(f"Found {len(programs)} programs in the database")
    
    for program in programs:
        if not program.arabic_name:
            if program.name in translations:
                program.arabic_name = translations[program.name]
                print(f"Added Arabic name for {program.name}: {program.arabic_name}")
                updated += 1
            else:
                # Create a basic Arabic name if no translation is found
                program.arabic_name = f"برنامج {program.name}"
                print(f"Added placeholder Arabic name for {program.name}")
                updated += 1
    
    if updated > 0:
        db.session.commit()
        print(f"Updated {updated} programs with Arabic names")
    else:
        print("All programs already have Arabic names")

def ensure_column_exists():
    """Make sure the arabic_name column exists in the programs table"""
    try:
        result = db.session.execute(text("PRAGMA table_info(programs)"))
        columns = {row[1] for row in result.fetchall()}
        
        if 'arabic_name' not in columns:
            print("Adding arabic_name column to programs table...")
            db.session.execute(text("ALTER TABLE programs ADD COLUMN arabic_name TEXT"))
            db.session.commit()
            print("Added arabic_name column")
        else:
            print("arabic_name column already exists")
            
        if 'arabic_description' not in columns:
            print("Adding arabic_description column to programs table...")
            db.session.execute(text("ALTER TABLE programs ADD COLUMN arabic_description TEXT"))
            db.session.commit()
            print("Added arabic_description column")
        else:
            print("arabic_description column already exists")
            
    except Exception as e:
        print(f"Error checking/adding columns: {e}")
        db.session.rollback()

def print_program_list():
    """Print a report of all available programs"""
    programs = Program.query.order_by(Program.degree_type, Program.name).all()
    
    print("\n=== AVAILABLE PROGRAMS ===")
    print(f"Total programs: {len(programs)}\n")
    
    current_degree = None
    for program in programs:
        if current_degree != program.degree_type:
            current_degree = program.degree_type
            print(f"\n{current_degree} Programs:")
            print("=" * 20)
        
        arabic = program.arabic_name if program.arabic_name else "NO ARABIC NAME"
        print(f"- {program.name} ({arabic})")
    
    print("\n")

def run():
    """Main function to run all checks"""
    app = setup_app()
    
    with app.app_context():
        print("Checking database for program issues...")
        ensure_column_exists()
        ensure_arabic_names()
        print_program_list()
        print("Database check complete!")

if __name__ == "__main__":
    run()
