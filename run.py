# --- Standard Libraries ---
import os
import json
import sys
import traceback
import logging
import time
from datetime import datetime, UTC, date
import click
from functools import wraps

# --- Third-Party Libraries ---
from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify, session,
    send_from_directory, current_app
)
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import requests  # For calling Gemini API
from sqlalchemy import text
from sqlalchemy.orm import joinedload, selectinload  # Add selectinload
from markupsafe import Markup, escape

# --- Conditional Import for PDF Processing ---
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("Warning: PyMuPDF (fitz) not installed. PDF text extraction will be disabled.")

# --- Application Models ---
from models import (
    db, User, Application, Document, Certificate,
    Payment, Project, News, Course, CourseEnrollment,
    Ticket, TicketMessage, Notification, StudentID, Program, ProgramCourse
)

# Configure logging for better debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Define the form class before it's used
class NewApplicationForm(FlaskForm):
    degree_type = SelectField('Degree Type', validators=[DataRequired()], 
                            choices=[('Diploma', 'Diploma'), ('Master', 'Master'), ('PhD', 'PhD')])
    program = SelectField('Program', validators=[DataRequired()], choices=[])  # Initialize with empty list
    academic_year = SelectField('Academic Year', validators=[DataRequired()], choices=[])  # Initialize with empty list
    semester = SelectField('Semester', validators=[DataRequired()], 
                         choices=[('1', 'First Semester'), ('2', 'Second Semester')])
    submit = SubmitField('تقديم الطلب النهائي')  # Updated label to match Arabic UI

# Initialize Flask app
app = Flask(__name__)

# Configure app with proper paths
app.config.update(
    SECRET_KEY='your-secret-key-goes-here',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///cu_project.db',  # Corrected from '#' to '///'
    UPLOAD_FOLDER=os.path.join('static', 'uploads')
)
# Ensure instance and uploads directories exist
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.template_filter('time_ago')
def time_ago_filter(time):
    """Format a timestamp as 'time ago' (e.g., "3 hours ago")"""
    now = datetime.now(UTC)

    # Make the input time timezone-aware if it's naive
    if time.tzinfo is None:
        time = time.replace(tzinfo=UTC)

    diff = now - time

    seconds = diff.total_seconds()

    if seconds < 3600:  # Less than an hour
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        return time.strftime("%Y-%m-%d")



@app.template_filter('initials')
def initials_filter(name):
    if not name:
        return "UN"

    parts = name.split()
    if len(parts) == 1:
        return parts[0][0].upper()
    else:
        return (parts[0][0] + parts[-1][0]).upper()


@app.template_filter('slice')
def slice_filter(iterable, start, end=None):
    if end is None:
        return iterable[start:]
    return iterable[start:end]


@app.template_filter('format_date')
def format_date_filter(date):
    if date is None:
        return ""
    try:
        return date.strftime("%b %d, %Y")
    except:
        return str(date)

# Add a template filter to convert newlines to <br> tags
@app.template_filter('nl2br')
def nl2br_filter(text):
    if not text:
        return ""
    return Markup(escape(text).replace('\n', '<br>\n'))

@app.route('/')
def index():
    # Get only active and featured projects for the homepage
    featured_projects = Project.query.filter_by(
        is_active=True,
        is_popular=True
    ).order_by(
        Project.created_at.desc()
    ).limit(3).all()

    # Fetch news items (tagged as 'news')
    news_items = News.query.filter_by(type='news', is_active=True)\
        .order_by(News.date.desc()).limit(3).all()

    # Fetch announcements (tagged as 'announcement')
    announcements = News.query.filter_by(type='announcement', is_active=True)\
        .order_by(News.date.desc()).limit(4).all()

    return render_template('index.html',
                          featured_projects=featured_projects,
                          news_items=news_items,
                          announcements=announcements)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('student_dashboard'))

    class LoginForm(FlaskForm):
        pass  # Empty form just for CSRF protection

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard' if user.is_admin() else 'student_dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

    # Add this new route to manually create admin user
@app.route('/create-admin', methods=['GET'])
def create_admin():
    # Check if admin user exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='admin'
        )
        admin.set_password('adminpassword')
        db.session.add(admin)
        db.session.commit()
        return 'Admin user created successfully!'
    else:
        # Reset admin password
        admin.set_password('adminpassword')
        db.session.commit()
        return 'Admin user password reset to "adminpassword"'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard'))

    class RegisterForm(FlaskForm):
        pass  # Empty form just for CSRF protection

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        full_name = request.form.get('fullName')
        phone = request.form.get('phone')
        nationality = request.form.get('nationality')
        education = request.form.get('education')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html', form=form)

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html', form=form)

        user = User(
            email=email,
            full_name=full_name,
            phone=phone,
            nationality=nationality,
            education=education
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('تم التسجيل بنجاح! الرجاء تسجيل الدخول.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/programs')
def programs():
    return render_template('programs.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin/applications')
@login_required

def admin_applications():
    applications = Application.query.all()
    return render_template('admin/applications.html', applications=applications)

@app.route('/admin/application/<int:application_id>/<action>', methods=['POST'])
@login_required
def admin_application_action(application_id, action):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    try:
        application = Application.query.get_or_404(application_id)

        if action == 'approve':
            application.status = 'Documents Approved'
            message = 'Application documents approved successfully'
        elif action == 'reject':
            application.status = 'Documents Rejected'
            message = 'Application documents rejected'
        else:
            return jsonify({'success': False, 'message': 'Invalid action'}), 400

        # Create notification for student
        notification = Notification(
            user_id=application.user_id,
            message=f'Your application {application.app_id} has been {action}d.',
            read=False
        )

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': message,
            'new_status': application.status
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Add the missing route for sending notes
@app.route('/admin/application/send-note', methods=['POST'])
@login_required
def admin_send_note():
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    try:
        data = request.get_json()
        application_id = data.get('application_id')
        subject = data.get('subject')
        message_text = data.get('message')

        if not application_id or not subject or not message_text:
            return jsonify({'success': False, 'message': 'Missing required data'}), 400

        application = Application.query.get_or_404(application_id)
        student = application.user

        # Generate a unique ticket ID (consider if a separate note model is better)
        ticket_count = Ticket.query.count() + 1
        ticket_id_str = f"NOTE-{ticket_count:03d}"

        # Create a new ticket to represent the note
        new_ticket = Ticket(
            ticket_id=ticket_id_str,
            user_id=student.id,
            subject=subject,
            status='Open' # Change status to Open instead of Closed
        )
        db.session.add(new_ticket)
        db.session.flush() # Get the ID before committing

        # Add the message from the admin
        admin_message = TicketMessage(
            ticket_id=new_ticket.id,
            sender='Admin',
            message=message_text,
            created_at=datetime.now(UTC)
        )
        db.session.add(admin_message)

        # Create notification for the student
        notification = Notification(
            user_id=student.id,
            message=f'New note regarding your application {application.app_id}: {subject}',
            read=False
        )
        db.session.add(notification)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Note sent successfully'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error sending note: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error sending note: {str(e)}'}), 500


@app.route('/admin/enrollments')
@login_required
def admin_enrollments():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    # Get applications with paid status that need student IDs
    enrollments = db.session.query(Application).filter_by(
        status='Documents Approved',
        payment_status='Paid'
    ).outerjoin(
        StudentID,
        Application.id == StudentID.application_id
    ).filter(
        StudentID.id == None
    ).all()

    # Get applications with student IDs
    enrolled_students = db.session.query(Application, StudentID).join(
        StudentID,
        Application.id == StudentID.application_id
    ).all()

    return render_template('admin/enrollments.html',
                          enrollments=enrollments,
                          enrolled_students=enrolled_students)

@app.route('/admin/generate_student_id/<int:app_id>', methods=['POST'])
@login_required
def generate_student_id(app_id):
    start_time = time.time()
    current_app.logger.info(f"Generating ID for app_id {app_id} - START")

    # --- Your existing logic ---
    # 1. Fetch application/user data
    db_fetch_start = time.time()
    application = Application.query.get_or_404(app_id)
    db_fetch_end = time.time()
    current_app.logger.info(f"Database fetch took: {db_fetch_end - db_fetch_start:.4f}s")

    # 2. Generate the ID string
    id_gen_start = time.time()
    year = datetime.now(UTC).year
    is_international = application.user.nationality != 'Egyptian'
    prefix = 'INT-' if is_international else 'LOC-'

    # Get program code
    program_code = ''.join(word[0].upper() for word in application.program.split())

    # Get latest ID for this year and type
    latest_student = StudentID.query.filter(
        StudentID.student_id.like(f'{year}-{prefix}{program_code}%')
    ).order_by(StudentID.student_id.desc()).first()

    if latest_student:
        last_number = int(latest_student.student_id.split('-')[-1])
        new_number = f"{last_number + 1:04d}"
    else:
        new_number = "0001"

    # Create new student ID
    new_student_id_str = f"{year}-{prefix}{program_code}-{new_number}"
    id_gen_end = time.time()
    current_app.logger.info(f"ID generation logic took: {id_gen_end - id_gen_start:.4f}s")

    # 3. Save to database
    db_save_start = time.time()
    # Remove user_id=application.user_id from the constructor call
    new_id_entry = StudentID(application_id=app_id, student_id=new_student_id_str)
    db.session.add(new_id_entry)

    # Create notification for student
    notification = Notification(
        user_id=application.user_id, # Keep user_id here for the Notification
        message=f'تم إنشاء رقم الطالب الخاص بك: {new_student_id_str}',
        read=False
    )
    db.session.add(notification)

    # Update application status
    application.status = 'Enrolled'

    db.session.commit()
    db_save_end = time.time()
    current_app.logger.info(f"Database save took: {db_save_end - db_save_start:.4f}s")
    # --- End of your logic ---

    end_time = time.time()
    current_app.logger.info(f"Generating ID for app_id {app_id} - END | Total time: {end_time - start_time:.4f}s")

    return jsonify(success=True, student_id=new_student_id_str, message="Student ID generated successfully.")

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied: Admin privileges required', 'danger')
        return redirect(url_for('student_dashboard'))

    # Get stats for dashboard
    applications_count = Application.query.filter_by(status='Pending Review').count()
    payment_pending_count = Application.query.filter_by(status='Documents Approved', payment_status='Pending').count()
    certificate_requests = Certificate.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()

    # Get recent applications and tickets
    recent_applications = Application.query.order_by(Application.date_submitted.desc()).limit(3).all()
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(3).all()

    # Get recent certificate requests
    recent_certificates = Certificate.query.order_by(Certificate.request_date.desc()).limit(3).all()

    return render_template('admin/dashboard.html',
                          applications_count=applications_count,
                          payment_pending_count=payment_pending_count,
                          certificate_requests=certificate_requests,
                          open_tickets=open_tickets,
                          recent_applications=recent_applications,
                          recent_tickets=recent_tickets,
                          recent_certificates=recent_certificates)






# Keep only this route (around line 380)
@app.route('/admin/certificates/update/<int:cert_id>', methods=['POST'])
@login_required
def admin_update_certificate(cert_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    try:
        certificate = Certificate.query.get_or_404(cert_id)

        # Update certificate status
        certificate.status = 'Ready for Pickup'

        # Create notification for student
        notification = Notification(
            user_id=certificate.user_id,
            message=f'Your certificate {certificate.cert_id} is ready for pickup.',
            read=False
        )

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'success': True,
            'cert_id': certificate.cert_id,
            'message': 'Certificate marked as ready for pickup'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        })


@app.route('/admin/certificates')
@login_required
def admin_certificates():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    # Get all certificates including pending payment ones
    certificates = Certificate.query.order_by(Certificate.request_date.desc()).all()

    return render_template('admin/certificates.html', certificates=certificates)


@app.route('/admin/tickets')
@login_required
def admin_tickets():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('admin/tickets.html', tickets=tickets)

@app.route('/admin/tickets/<int:ticket_id>')
@login_required
def admin_ticket_detail(ticket_id):
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('admin/ticket_detail.html', ticket=ticket)

@app.route('/admin/tickets/reply/<int:ticket_id>', methods=['POST'])
@login_required
def admin_ticket_reply(ticket_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        message_text = request.form.get('message')

        if not message_text:
            return jsonify({'success': False, 'message': 'Message cannot be empty'})

        # Create a new message
        new_message = TicketMessage(
            ticket_id=ticket.id,
            sender='Admin',
            message=message_text,
            created_at=datetime.now(UTC)
        )

        # Update ticket status to In Progress if it's Open
        if ticket.status == 'Open':
            ticket.status = 'In Progress'

        # Create notification for student
        notification = Notification(
            user_id=ticket.user_id,
            message=f'New reply to your ticket: {ticket.subject}',
            read=False
        )

        db.session.add(new_message)
        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Reply sent successfully',
            'data': {
                'message': message_text,
                'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M'),
                'sender': 'Admin'
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/tickets/update_status/<int:ticket_id>', methods=['POST'])
@login_required
def admin_update_ticket_status(ticket_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')

    if new_status in ['Open', 'In Progress', 'Closed']:
        ticket.status = new_status

        # Notify student of status change
        notification = Notification(
            user_id=ticket.user_id,
            message=f'Your ticket {ticket.ticket_id} status has been updated to {new_status}.'
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Invalid status'})

@app.route('/admin/settings')
@login_required
def admin_settings():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    # In a real app, you might load settings from a database
    settings = {
        'local_fee': 600,
        'international_fee': 1500,
        'certificate_fee': 200,
        'email_notifications': True,
        'sms_notifications': True,
        'push_notifications': False
    }

    return render_template('admin/settings.html', settings=settings)



# Student Routes
def calculate_gpa(user_id):
    """Calculate cumulative GPA for a student based on their course grades"""
    try: # Corrected syntax: replaced '{' with ':'
        # Try to query with the new column
        enrollments = CourseEnrollment.query.filter_by(student_id=user_id).all()

        if not enrollments:
            return None

        total_gpa_points = 0
        total_credits = 0

        for enrollment in enrollments:
            # Skip courses without grades or in progress
            if not enrollment.grade or enrollment.status != 'Completed':
                continue

            # Get course credits using Session.get instead of Query.get
            course = db.session.get(Course, enrollment.course_id)
            if not course:
                continue

            # GPA value mapping
            gpa_map = {
                'A+': 4.0, 'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'F': 0.0
            }

            # Use the existing gpa_value if available, otherwise calculate from grade
            gpa_value = 0.0 # Initialize gpa_value
            try:
                # Check if the enrollment object has the gpa_value attribute
                if hasattr(enrollment, 'gpa_value') and enrollment.gpa_value is not None:
                    gpa_value = enrollment.gpa_value
                else:
                    # Fallback to calculating from grade if gpa_value is missing or None
                    gpa_value = gpa_map.get(enrollment.grade, 0.0)
            except AttributeError:
                # Handle cases where the gpa_value column might not exist yet
                app.logger.warning(f"Enrollment ID {enrollment.id} missing gpa_value attribute. Calculating from grade.")
                gpa_value = gpa_map.get(enrollment.grade, 0.0)

            # Add to total GPA calculation
            total_gpa_points += gpa_value * course.credits
            total_credits += course.credits

        # Return None if no completed courses with grades
        if total_credits == 0:
            return None

        # Calculate and return GPA, handle division by zero
        cumulative_gpa = round(total_gpa_points / total_credits, 2) if total_credits > 0 else 0.0
        return cumulative_gpa

    except Exception as e:
        app.logger.error(f"Error calculating GPA for user {user_id}: {str(e)}", exc_info=True)
        # Return None in case of error
        return None

def get_current_academic_year():
    today = date.today()
    # Simple logic: If before August 1st, it's part of the previous academic year start
    if today.month < 8:
        return f"{today.year - 1}-{today.year}"
    else:
        return f"{today.year}-{today.year + 1}"

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    applications = Application.query.filter_by(user_id=current_user.id).all()
    documents = Document.query.filter_by(user_id=current_user.id).all()
    certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()

    # Get unread notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, read=False).order_by(Notification.created_at.desc()).all()

    # Check if there are any applications with approved documents that need payment
    payment_required = any(app.status == 'Documents Approved' and app.payment_status == 'Pending' for app in applications)

    # Check if there are any certificates ready for pickup
    certificate_ready = any(cert.status == 'Ready for Pickup' for cert in certificates)

    # Get student ID and program info
    student_id_obj = StudentID.query.join(Application).filter(
        Application.user_id == current_user.id
    ).first()

    student_id = student_id_obj.student_id if student_id_obj else None
    program = student_id_obj.application.program if student_id_obj else None

    # Calculate cumulative GPA
    cumulative_gpa = calculate_gpa(current_user.id)

    # Calculate total credits (for the dashboard)
    total_credits = 0
    try:
        # Use raw SQL to avoid ORM querying columns that might not exist yet
        sql_query = text("SELECT ce.course_id FROM course_enrollments ce WHERE ce.student_id = :student_id AND ce.status = :status")
        result = db.session.execute(sql_query, {"student_id": current_user.id, "status": "Completed"})
        course_ids = [row[0] for row in result]

        # Now get the credits for each course
        for course_id in course_ids:
            course = db.session.get(Course, course_id)
            if course:
                total_credits += course.credits
    except Exception as e:
        print(f"Error calculating credits: {str(e)}")

    return render_template(
        'student/dashboard.html',
        applications=applications,
        documents=documents,
        certificates=certificates,
        tickets=tickets,
        notifications=notifications,
        payment_required=payment_required,
        certificate_ready=certificate_ready,
        student_id=student_id,
        program=program,
        cumulative_gpa=cumulative_gpa,
        total_credits=total_credits
    )

@app.route('/student/applications')
@login_required
def student_applications():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('student/applications.html', applications=applications)

@app.route('/student/new_application', methods=['GET', 'POST'])
@login_required
def student_new_application():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    form = NewApplicationForm()
    
    # Initialize academic_year choices for the current and next 2 years
    current_year = datetime.now(UTC).year
    academic_years = [(f"{year}/{year+1}", f"{year}/{year+1}") for year in range(current_year, current_year + 3)]
    form.academic_year.choices = academic_years

    if request.method == 'POST':
        app.logger.info("--- New Application POST Request Received ---")
        
        degree_type = request.form.get('degree_type')
        program_json = request.form.get('program')
        academic_year = request.form.get('academic_year')
        semester = request.form.get('semester')
        
        # Get document files
        document_files = request.files.getlist('document_files[]')
        document_types = request.form.getlist('document_types[]')

        app.logger.info(f"Received degree_type: '{degree_type}'")
        app.logger.info(f"Received program_json: '{program_json}'")
        app.logger.info(f"Received academic_year: '{academic_year}'")
        app.logger.info(f"Received semester: '{semester}'")
        app.logger.info(f"Received {len(document_files)} document files and {len(document_types)} document types")

        # Check if any program field is None or empty
        if not all([degree_type, program_json, academic_year, semester]):
            flash('جميع حقول البرنامج مطلوبة', 'danger')
            
            # Repopulate choices for form display
            if degree_type:
                try:
                    programs = Program.query.filter_by(degree_type=degree_type).order_by(Program.name).all()
                    program_choices = [(json.dumps({'id': p.id, 'name': p.name, 'degree_type': p.degree_type, 'arabic_name': p.arabic_name}), f"{p.name} {f'({p.arabic_name})' if p.arabic_name else ''}") for p in programs]
                    form.program.choices = program_choices
                except Exception as e:
                    app.logger.error(f"Error repopulating program choices: {str(e)}")
                    form.program.choices = []
            else:
                form.program.choices = []
            
            return render_template('student/new_application.html', form=form, now=datetime.now(UTC))

        # Check if documents are provided
        if len(document_files) == 0 or len(document_types) == 0 or len(document_files) != len(document_types):
            flash('المستندات المطلوبة غير مكتملة', 'danger')
            return render_template('student/new_application.html', form=form, now=datetime.now(UTC))

        # Populate form choices for validation
        try:
            # Set program choices with the submitted program
            if program_json:
                try:
                    program_data = json.loads(program_json)
                    form.program.choices = [(program_json, program_json)]
                except json.JSONDecodeError:
                    form.program.choices = []
                    app.logger.warning(f"Invalid program JSON: {program_json}")
            else:
                form.program.choices = []

            # Make sure academic year choices are populated
            if not form.academic_year.choices:
                form.academic_year.choices = academic_years
        except Exception as e:
            app.logger.error(f"Error setting form choices: {str(e)}", exc_info=True)
            form.program.choices = []

        # Validate the form
        if form.validate_on_submit():
            app.logger.info("Form validation passed.")
            try:
                # Begin a database transaction
                db.session.begin_nested()  # Create a savepoint
                
                # Process the application data
                program_info = json.loads(program_json)
                program_id = program_info.get('id')
                program_db = db.session.get(Program, program_id) if program_id else None
                program_type = program_db.type if program_db and hasattr(program_db, 'type') else 'Professional'
                
                # Build program display name
                program_name_display = program_info.get('name', '')
                arabic_name = program_info.get('arabic_name')
                
                if arabic_name:
                    program_name_display = f"{arabic_name} ({program_name_display})"
                else:
                    program_name_display = f"{program_info.get('degree_type')} - {program_name_display}"
                
                # Create unique application ID
                app_count = Application.query.count() + 1
                app_id = f"APP-{datetime.now(UTC).strftime('%Y%m%d')}-{app_count:04d}"
                
                # Create application record
                application = Application(
                    app_id=app_id,
                    user_id=current_user.id,
                    program=program_name_display,
                    program_id=program_id,
                    status='Pending Review',
                    date_submitted=datetime.now(UTC),
                    academic_year=academic_year,
                    semester=semester,
                    program_type=program_type
                )
                
                db.session.add(application)
                db.session.flush()  # Get application ID without committing
                
                # Process document uploads
                for i, file in enumerate(document_files):
                    if file and file.filename:
                        doc_type = document_types[i] if i < len(document_types) else "unknown"
                        
                        # Create a unique filename
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
                        new_filename = f"{current_user.id}_{timestamp}_{i}_{filename}"
                        
                        # Save file
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                        file.save(file_path)
                        
                        # Create document record
                        document = Document(
                            user_id=current_user.id,
                            application_id=application.id,
                            name=doc_type,  # Use document type as name
                            file_path=f"uploads/{new_filename}",
                            status='Uploaded',
                            uploaded_at=datetime.now(UTC)
                        )
                        
                        db.session.add(document)
                
                # Commit all changes
                db.session.commit()
                
                app.logger.info(f"Application {app_id} with {len(document_files)} documents submitted successfully for user {current_user.id}")
                flash('تم تقديم طلبك بنجاح مع المستندات المطلوبة!', 'success')
                return redirect(url_for('student_applications'))
                
            except json.JSONDecodeError:
                app.logger.error("JSONDecodeError processing program data.", exc_info=True)
                flash('خطأ في بيانات البرنامج المختار.', 'danger')
                db.session.rollback()
                return render_template('student/new_application.html', form=form, now=datetime.now(UTC))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error submitting application: {str(e)}", exc_info=True)
                flash('حدث خطأ أثناء تقديم الطلب. الرجاء المحاولة مرة أخرى.', 'danger')
                return render_template('student/new_application.html', form=form, now=datetime.now(UTC))
        else:
            app.logger.warning(f"Form validation failed. Errors: {form.errors}")
            flash('هناك أخطاء في النموذج. يرجى التحقق من الحقول.', 'danger')
            return render_template('student/new_application.html', form=form, now=datetime.now(UTC))

    # GET request handling
    return render_template('student/new_application.html', form=form, now=datetime.now(UTC))

# Helper function to determine required documents (move this or define appropriately)
def get_required_documents_list(degree_type, nationality):
    """Returns a list of required document dicts {name: '...', type: '...'}"""
    base_docs = [
        {"name": "صورة شخصية حديثة", "type": "photo"},
        {"name": "شهادة الميلاد", "type": "birth_certificate"},
        {"name": "شهادة الثانوية العامة", "type": "high_school_cert"},
        {"name": "شهادة البكالوريوس", "type": "bachelor_cert"},
        {"name": "السجل الأكاديمي (كشف الدرجات)", "type": "transcript"},
    ]
    if degree_type in ['Master', 'PhD']:
        base_docs.append({"name": "خطاب توصية (1)", "type": "recommendation_1"})
        base_docs.append({"name": "خطاب توصية (2)", "type": "recommendation_2"})
        base_docs.append({"name": "السيرة الذاتية", "type": "cv"})
    if degree_type == 'PhD':
         base_docs.append({"name": "شهادة الماجستير", "type": "master_cert"})
         base_docs.append({"name": "مقترح بحثي", "type": "research_proposal"})

    if nationality == 'Egyptian':
        base_docs.append({"name": "بطاقة الرقم القومي", "type": "national_id"})
        # Add military status document for males if needed
        # base_docs.append({"name": "شهادة الموقف من التجنيد", "type": "military_status"})
    else: # International
        base_docs.append({"name": "جواز السفر", "type": "passport"})
        base_docs.append({"name": "شهادة إجادة اللغة الإنجليزية (إن وجدت)", "type": "english_proficiency"})

    return base_docs

@app.route('/student/documents')
@login_required
def student_documents():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    documents = Document.query.filter_by(user_id=current_user.id).all()
    applications = Application.query.filter_by(user_id=current_user.id).all()

    return render_template('student/documents.html', documents=documents, applications=applications)

@app.route('/student/documents/upload', methods=['GET', 'POST'])
@login_required
def student_upload_document():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    # Add a FlaskForm for CSRF protection
    class DocumentForm(FlaskForm):
        pass  # Empty form just for CSRF protection

    form = DocumentForm()

    if request.method == 'POST' and form.validate_on_submit():
        document_type = request.form.get('document_type')
        application_id = request.form.get('application_id')

        if 'document' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['document']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            # Create a unique filename with timestamp
            timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
            new_filename = f"{current_user.id}_{timestamp}_{filename}"

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

            # Create document record
            new_document = Document(
                user_id=current_user.id,
                application_id=application_id if application_id else None,
                name=document_type,
                file_path=f"uploads/{new_filename}",
                status='Uploaded'
            )

            db.session.add(new_document)
            db.session.commit()

            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('student_documents'))

    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('student/upload_document.html', form=form, applications=applications)

@app.route('/student/document/delete/<int:doc_id>', methods=['POST'])
@login_required
def student_delete_document(doc_id):
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    document = Document.query.get_or_404(doc_id)

    # Ensure this document belongs to the current user
    if document.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('student_documents'))

    # Get the file path to remove it from storage
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.file_path.replace('uploads/', ''))

    # Delete the document from the database
    db.session.delete(document)
    db.session.commit()

    # Try to remove the file (if it exists)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # Log the error but continue (document is already deleted from database)
        print(f"Error removing file: {e}")

    flash('Document deleted successfully', 'success')
    return redirect(url_for('student_documents'))

@app.route('/student/certificates')
@login_required
def student_certificates():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    return render_template('student/certificates.html', certificates=certificates)


# Keep the original route
@app.route('/student/certificates/request', methods=['GET', 'POST'])
@login_required
def student_request_certificate():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    # Add a FlaskForm for CSRF protection
    class CertificateForm(FlaskForm):
        pass  # Empty form just for CSRF protection

    form = CertificateForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Create new certificate request
        certificate = Certificate(
            user_id=current_user.id,
            type=request.form.get('certificate_type'),
            purpose=request.form.get('purpose'),
            copies=int(request.form.get('copies', 1)),
            status='Pending Payment',
            cert_id=f"CERT-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            request_date=datetime.now(UTC)
        )

        db.session.add(certificate)
        db.session.commit()

        flash('تم تقديم طلب الشهادة بنجاح!', 'success')
        return redirect(url_for('student_certificates'))

    return render_template('student/request_certificate.html', form=form)

@app.route('/student/support')
@login_required
def student_support():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    return render_template('student/support.html', tickets=tickets)

@app.route('/student/support/new', methods=['GET', 'POST'])
@login_required
def student_new_ticket():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not subject or not message:
            flash('Please fill out all fields', 'danger')
            return redirect(request.url)

        # Generate a unique ticket ID
        ticket_count = Ticket.query.count() + 1
        ticket_id = f"TKT-{ticket_count:03d}"

        # Create new ticket
        new_ticket = Ticket(
            ticket_id=ticket_id,
            user_id=current_user.id,
            subject=subject,
            status='Open'
        )

        db.session.add(new_ticket)
        db.session.commit()

        # Add the first message
        first_message = TicketMessage(
            ticket_id=new_ticket.id,
            sender='Student',
            message=message
        )

        db.session.add(first_message)
        db.session.commit()

        flash('Support ticket submitted successfully!', 'success')
        return redirect(url_for('student_support'))

    return render_template('student/new_ticket.html')

@app.route('/student/support/<int:ticket_id>')
@login_required
def student_ticket_detail(ticket_id):
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)

    # Ensure this ticket belongs to the current user
    if ticket.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('student_support'))

    return render_template('student/ticket_detail.html', ticket=ticket)

@app.route('/student/support/reply/<int:ticket_id>', methods=['POST'])
@login_required
def student_ticket_reply(ticket_id):
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    try:
        ticket = Ticket.query.get_or_404(ticket_id)

        # Ensure ticket belongs to current user
        if ticket.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Access denied'})

        message_text = request.form.get('message')
        if not message_text:
            return jsonify({'success': False, 'message': 'Message cannot be empty'})

        # Create new message
        new_message = TicketMessage(
            ticket_id=ticket.id,
            sender='Student',
            message=message_text,
            created_at=datetime.now(UTC)
        )

        # Create notification for admins
        admins = User.query.filter_by(role='admin').all()
        for admin in admins:
            notification = Notification(
                user_id=admin.id,
                message=f'New reply on ticket {ticket.ticket_id} from {current_user.full_name}',
                read=False
            )
            db.session.add(notification)

        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Reply sent successfully',
            'data': {
                'message': message_text,
                'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M'),
                'sender': 'Student'
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/student/payments/<int:app_id>', methods=['GET', 'POST'])
@login_required
def student_payment(app_id):
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    application = Application.query.get_or_404(app_id)

    # Create empty form for CSRF protection
    form = FlaskForm()

    # Ensure this application belongs to the current user
    if application.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('student_applications'))

    if request.method == 'POST' and form.validate_on_submit():
        # Calculate fee based on nationality
        fee = 1500 if current_user.nationality == 'International' else 600

        # Create payment record
        new_payment = Payment(
            user_id=current_user.id,
            application_id=application.id,
            amount=fee,
            payment_method='Simulation',
            transaction_id=f"TXN-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
        )

        # Update application payment status
        application.payment_status = 'Paid'

        db.session.add(new_payment)
        db.session.commit()

        flash('تم معالجة الدفع بنجاح!', 'success')
        return redirect(url_for('student_applications'))

    # Calculate fee based on nationality
    fee = 1500 if current_user.nationality == 'International' else 600

    return render_template('student/payment.html',
                         application=application,
                         fee=fee)

@app.route('/student/certificate_payment/<int:cert_id>', methods=['GET', 'POST'])
@login_required
def student_certificate_payment(cert_id):
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    certificate = Certificate.query.get_or_404(cert_id)

    # Create empty form for CSRF protection
    class PaymentForm(FlaskForm):
        pass

    form = PaymentForm()

    # Ensure certificate belongs to current user
    if certificate.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('student_certificates'))

    return render_template('student/settings.html')

@app.route('/student/settings')
@login_required
def student_settings():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    # Create a form for CSRF protection
    class SettingsForm(FlaskForm):
        pass
    
    form = SettingsForm()
    
    return render_template('student/settings.html', form=form)

@app.route('/student/settings/update', methods=['POST'])
@login_required
def student_update_settings():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    full_name = request.form.get('full_name')
    phone = request.form.get('phone')

    current_user.full_name = full_name
    current_user.phone = phone

    db.session.commit()

    flash('Settings updated successfully!', 'success')
    return redirect(url_for('student_settings'))

@app.route('/student/change_password', methods=['POST'])
@login_required
def student_change_password():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_user.check_password(current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('student_settings'))

    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('student_settings'))

    current_user.set_password(new_password)
    db.session.commit()

    flash('Password changed successfully!', 'success')
    return redirect(url_for('student_settings'))

@app.route('/mark_notifications_read', methods=['POST'])
@login_required
def mark_notifications_read():
    notifications = Notification.query.filter_by(user_id=current_user.id, read=False).all()

    for notification in notifications:
        notification.read = True

    db.session.commit()
    return jsonify({'success': True})

@app.route('/student/close_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def student_close_ticket(ticket_id):
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)

    # Ensure this ticket belongs to the current user
    if ticket.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('student_support'))

    ticket.status = 'Closed'
    db.session.commit()

    flash('Ticket closed successfully', 'success')
    return redirect(url_for('student_ticket_detail', ticket_id=ticket.id))

@app.route('/student/update_notification_preferences', methods=['POST'])
@login_required
def student_update_notification_preferences():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    # In a real app, you would update user preferences in the database
    flash('Notification preferences updated successfully!', 'success')
    return redirect(url_for('student_settings'))

# Add this new route for student profile

@app.route('/student/profile', methods=['GET'])
@login_required
def student_profile():
    """Display student profile page"""
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    # Get student ID if available
    student_id = None
    if hasattr(current_user, 'student_id') and current_user.student_id:
        student_id = current_user.student_id
    
    # Get program if available - use Application instead of Enrollment
    program = None
    student_id_obj = StudentID.query.join(Application).filter(
        Application.user_id == current_user.id
    ).first()
    
    if student_id_obj and student_id_obj.application:
        program = student_id_obj.application.program
    
    return render_template('student/profile.html', 
                          student_id=student_id,
                          program=program)

# Add a new route for updating profile
@app.route('/student/profile/update', methods=['POST'])
@login_required
def student_update_profile():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    address = request.form.get('address')

    current_user.full_name = full_name
    current_user.phone = phone
    current_user.address = address

    db.session.commit()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('student_profile'))

# Add this new command function
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database and create admin user."""
    db.create_all()

    # Check if admin user exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='admin'
        )
        admin.set_password('adminpassword')
        db.session.add(admin)
        db.session.commit()
        click.echo('Initialized the database and created admin user.')
    else:
        click.echo('Database already initialized.')




@app.route('/admin/projects')
@login_required
def admin_projects():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)



@app.route('/admin/projects/new', methods=['GET', 'POST'])
@login_required
def admin_new_project():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        url = request.form.get('url')
        is_popular = 'is_popular' in request.form
        is_active = 'is_active' in request.form

        # Handle file upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in file.filename and \
                   file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:

                    # Create unique filename
                    timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
                    original_filename = secure_filename(file.filename)
                    new_filename = f"project_{timestamp}_{original_filename}"

                    # Ensure upload directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                    # Save file
                    try:
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                        file.save(file_path)
                        image_path = 'uploads/' + new_filename
                    except Exception as e:
                        flash(f'Error uploading file: {str(e)}', 'danger')
                        return redirect(url_for('admin_new_project'))
                else:
                    flash('Invalid file type. Please upload an image file.', 'danger')
                    return redirect(url_for('admin_new_project'))

        try:
            # Create new project
            new_project = Project(
                title=title,
                description=description,
                category=category,
                url=url,
                image_path=image_path,
                is_popular=is_popular,
                is_active=is_active,
                user_id=current_user.id
            )

            db.session.add(new_project)
            db.session.commit()

            flash('Project added successfully!', 'success')
            return redirect(url_for('admin_projects'))

        except Exception as e:
            # If there's an error saving to database, delete uploaded file
            if image_path:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                except:
                    pass
            db.session.rollback()
            flash(f'Error creating project: {str(e)}', 'danger')
            return redirect(url_for('admin_new_project'))

    # GET request - show form
    return render_template('admin/new_project.html')


@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(project_id):
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category = request.form.get('category')
        project.url = request.form.get('url')
        project.is_popular = 'is_popular' in request.form
        project.is_active = 'is_active' in request.form

        # Handle file upload if there's a new image
        if 'project_image' in request.files:
            file = request.files['project_image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                # Create a unique filename with timestamp
                timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
                new_filename = f"project_{timestamp}_{filename}"

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

                # Delete the old image if it exists
                if project.image_path:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                                project.image_path.replace('uploads/', ''))
                    try:
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    except Exception as e:
                        print(f"Error removing old image: {e}")

                project.image_path = f"uploads/{new_filename}"

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))

    return render_template('admin/edit_project.html', project=project)

@app.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def admin_delete_project(project_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    project = Project.query.get_or_404(project_id)

    # Delete image file if it exists
    if project.image_path:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                               project.image_path.replace('uploads/', ''))
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file: {e}")

    db.session.delete(project)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/admin/projects/toggle-status/<int:project_id>', methods=['POST'])
@login_required
def admin_toggle_project_status(project_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    project = Project.query.get_or_404(project_id)
    status_type = request.form.get('status_type')

    if status_type == 'active':
        project.is_active = not project.is_active
        status_message = 'active' if project.is_active else 'inactive'
    elif status_type == 'popular':
        project.is_popular = not project.is_popular
        status_message = 'popular' if project.is_popular else 'not popular'

    db.session.commit()
    return jsonify({'success': True, 'status': status_message})


@app.route('/projects')
def projects():
    # Get all active projects
    projects = Project.query.filter_by(is_active=True).order_by(Project.created_at.desc()).all()

    # Get unique categories
    categories = db.session.query(Project.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]

    return render_template('projects.html',
                         projects=projects,
                         categories=categories)

# Register the command with Flask CLI
app.cli.add_command(init_db_command)

@app.context_processor
def inject_now():
    return {'now': datetime.now(UTC)}

@app.route('/news')
def news():
    news_items = News.query.order_by(News.date.desc()).all()
    return render_template('news.html', news_items=news_items)

@app.route('/admin/news')
@login_required
def admin_news():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    news_items = News.query.order_by(News.date.desc()).all()
    return render_template('admin/news.html', news_items=news_items)

@app.route('/admin/news/add', methods=['GET', 'POST'])
@login_required
def admin_news_add():
    class NewsForm(FlaskForm):
        pass

    form = NewsForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        news_type = request.form.get('type')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
                new_filename = f"news_{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                image_path = f"uploads/{new_filename}"

        news_item = News(
            title=title,
            description=description,
            type=news_type,
            date=date,
            image_path=image_path
        )

        db.session.add(news_item)
        db.session.commit()

        flash('News item added successfully!', 'success')
        return redirect(url_for('admin_news'))

    return render_template('admin/news_add.html', form=form)

@app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_news_edit(id):
    class NewsForm(FlaskForm):
        pass

    form = NewsForm()
    news_item = News.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit():
        news_item.title = request.form.get('title')
        news_item.description = request.form.get('description')
        news_item.type = request.form.get('type')
        news_item.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Delete old image if exists
                if news_item.image_path:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                                news_item.image_path.replace('uploads/', ''))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                filename = secure_filename(file.filename)
                timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
                new_filename = f"news_{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                news_item.image_path = f"uploads/{new_filename}"

        db.session.commit()
        flash('News item updated successfully!', 'success')
        return redirect(url_for('admin_news'))

    return render_template('admin/news_edit.html', form=form, news=news_item)

@app.route('/admin/news/delete/<int:id>', methods=['POST'])
@login_required
def admin_news_delete(id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    news_item = News.query.get_or_404(id)

    # Delete image file if exists
    if news_item.image_path:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                news_item.image_path.replace('uploads/', ''))
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(news_item)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/about')
def about():
    """Display about page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Display contact page"""
    return render_template('contact.html')

@app.route('/search')
def search():
    """Handle search functionality"""
    query = request.args.get('q', '')
    # Implement search logic here
    results = []  # Replace with actual search results
    return render_template('search.html', results=results, query=query)

@app.route('/faq')
def faq():
    """Display FAQ page"""
    return render_template('faq.html')

@app.route('/privacy')
def privacy():
    """Display privacy policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Display terms of service page"""
    return render_template('terms.html')

@app.route('/student/courses')
@login_required
def student_courses():
    """Displays enrolled and available courses for the student, handling auto-enrollment."""
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    user_id = current_user.id
    current_academic_year = get_current_academic_year() # Get current academic year
    active_application = None # Initialize outside the try block

    # --- Automatic Semester Enrollment Logic ---
    try:
        # 1. Find the student's active/enrolled application and the semester they applied for
        active_application = Application.query.filter(
            Application.user_id == user_id,
            Application.status == 'Enrolled' # Ensure they are officially enrolled
        ).options(
            selectinload(Application.program_relation) # Eager load program
        ).order_by(Application.date_submitted.desc()).first()

        if active_application and active_application.program_relation and active_application.semester:
            program = active_application.program_relation
            # Determine target semester name based on application data
            # Assuming application.semester stores '1' or '2'
            target_semester_number = active_application.semester # Keep the number '1' or '2'
            target_semester_name = "First Semester" if target_semester_number == '1' else "Second Semester" if target_semester_number == '2' else None

            if target_semester_name and target_semester_number: # Check both number and name
                app.logger.info(f"User {user_id} enrolled in program {program.id}. Checking auto-enrollment for {target_semester_name} ({current_academic_year}).")

                # 2. Identify courses for the target semester in this program using the NUMBER
                target_semester_program_courses = ProgramCourse.query.filter_by(
                    program_id=program.id,
                    semester=int(target_semester_number) # Use the integer number for query
                ).all()

                target_course_ids = [pc.course_id for pc in target_semester_program_courses]

                if target_course_ids:
                    # 3. Check if student is already enrolled in ANY of these target semester courses for the CURRENT academic year
                    existing_enrollment_this_year = CourseEnrollment.query.filter(
                        CourseEnrollment.student_id == user_id, # Corrected from user_id
                        CourseEnrollment.course_id.in_(target_course_ids),
                        CourseEnrollment.academic_year == current_academic_year # Crucial check for idempotency per year
                    ).first()

                    # 4. If no existing enrollment found for this semester's courses in this academic year, enroll them
                    if not existing_enrollment_this_year:
                        enrollments_added = 0
                        for course_id in target_course_ids:
                            # Double-check just in case before adding
                            already_exists = CourseEnrollment.query.filter_by(
                                student_id=user_id, # Corrected from user_id
                                course_id=course_id,
                                academic_year=current_academic_year
                            ).first()

                            if not already_exists:
                                new_enrollment = CourseEnrollment(
                                    student_id=user_id, # Corrected from user_id
                                    course_id=course_id,
                                    program_id=program.id, # Store program context
                                    enrollment_date=datetime.now(UTC),
                                    status='Enrolled',
                                    semester=target_semester_name, # Store semester name for display consistency
                                    academic_year=current_academic_year # Store academic year context
                                )
                                db.session.add(new_enrollment)
                                enrollments_added += 1

                        if enrollments_added > 0:
                            db.session.commit()
                            flash(f'تم تسجيلك تلقائيًا في مقررات {target_semester_name} لبرنامجك ({enrollments_added} مقرر) للعام الدراسي {current_academic_year}.', 'success') # RTL message
                            app.logger.info(f"User {user_id} auto-enrolled in {enrollments_added} courses for {target_semester_name} ({current_academic_year}), program {program.id}.")
                        else:
                             app.logger.info(f"User {user_id} already enrolled in {target_semester_name} courses for {current_academic_year}, program {program.id}. No auto-enrollment needed.")
                    else:
                        app.logger.info(f"User {user_id} already has enrollments for {target_semester_name} ({current_academic_year}). Skipping auto-enrollment.")
                else:
                    # Use the number in the log message for clarity on what was queried
                    app.logger.warning(f"No courses found defined for Program ID {program.id}, Semester Number: {target_semester_number}.")
            else:
                 app.logger.warning(f"Could not determine target semester from application {active_application.id} (semester value: {active_application.semester}). Skipping auto-enrollment.")
        else:
            # Log reasons for skipping auto-enrollment if application details are missing
            if not active_application:
                 app.logger.info(f"User {user_id} has no 'Enrolled' application. Skipping auto-enrollment.")
            elif not active_application.program_relation:
                 app.logger.warning(f"Application {active_application.id if active_application else 'N/A'} for user {user_id} has no linked program. Skipping auto-enrollment.")
            elif not active_application.semester:
                 app.logger.warning(f"Application {active_application.id if active_application else 'N/A'} for user {user_id} is missing the 'semester' value. Skipping auto-enrollment.")


    except Exception as e:
        db.session.rollback() # Rollback in case of error during auto-enrollment
        app.logger.error(f"Error during automatic enrollment check for user {user_id}: {str(e)}", exc_info=True)
        flash('حدث خطأ أثناء التحقق من التسجيل التلقائي في المقررات.', 'danger') # RTL message

    # --- Fetch Courses for Display (After potential auto-enrollment) ---
    enrolled_courses_data = []
    available_courses_data = []
    enrolled_course_ids = set()

    try:
        # Fetch enrolled courses with details
        enrolled_items = db.session.query(
            Course, CourseEnrollment
        ).join(
            CourseEnrollment, Course.id == CourseEnrollment.course_id
        ).filter(
            CourseEnrollment.student_id == user_id # Corrected back to student_id
        ).options(
            joinedload(CourseEnrollment.course) # Eager load course details
        ).order_by(
            CourseEnrollment.academic_year.desc(),
            CourseEnrollment.semester,
            Course.code
        ).all()

        for course, enrollment in enrolled_items:
            enrolled_courses_data.append({
                'course': course,
                'enrollment': enrollment,
                'semester': enrollment.semester, # Display semester from enrollment record
                'academic_year': enrollment.academic_year # Display year from enrollment record
            })
            enrolled_course_ids.add(course.id)

        # Fetch available courses (courses in the student's program they are NOT enrolled in for the current year)
        # Re-fetch active application to get program info if not already fetched or if it was None initially
        if not active_application:
             active_application = Application.query.filter(
                Application.user_id == user_id,
                Application.status == 'Enrolled'
             ).options(selectinload(Application.program_relation)).order_by(Application.date_submitted.desc()).first()

        if active_application and active_application.program_relation:
            program = active_application.program_relation
            program_courses = ProgramCourse.query.filter_by(program_id=program.id).all()
            program_course_ids = {pc.course_id for pc in program_courses}

            # Find course IDs in the program but not in the enrolled set for the current year
            # We need to check enrollments specifically for the current year here
            enrolled_this_year_ids = {
                enrollment.course_id for course, enrollment in enrolled_items
                if enrollment.academic_year == current_academic_year
            }

            available_course_ids = program_course_ids - enrolled_this_year_ids

            if available_course_ids:
                 available_items = db.session.query(
                     Course, ProgramCourse.semester # Fetch semester from ProgramCourse
                 ).join(
                     ProgramCourse, Course.id == ProgramCourse.course_id
                 ).filter(
                     ProgramCourse.program_id == program.id,
                     Course.id.in_(list(available_course_ids)),
                     Course.is_active == True # Only show active courses
                 ).order_by(
                     ProgramCourse.semester, # Order by semester from ProgramCourse
                     Course.code
                 ).all()

                 for course, semester_name in available_items: # Use semester_name from query
                     # TODO: Add prerequisite check here if needed before showing as available
                     available_courses_data.append({
                         'course': course,
                         'semester': semester_name # Use semester name from ProgramCourse
                     })

    except Exception as e:
        app.logger.error(f"Error fetching course data for student {user_id}: {str(e)}", exc_info=True)
        flash('حدث خطأ أثناء تحميل بيانات المقررات.', 'danger')

    return render_template(
        'student/courses.html',
        enrolled_courses=enrolled_courses_data,
        available_courses=available_courses_data
    )

# Modify the manual enrollment route to include academic year and semester
@app.route('/student/courses/enroll/<int:course_id>', methods=['POST'])
@login_required
def student_course_enroll(course_id): # Renamed function for clarity
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    course = Course.query.get_or_404(course_id)
    if not course.is_active:
         return jsonify({'success': False, 'message': 'This course is currently inactive.'})

    user_id = current_user.id
    current_academic_year = get_current_academic_year()
    target_semester = "Unknown" # Default
    program_id = None

    # Find student's program and the semester this course belongs to
    active_application = Application.query.filter_by(user_id=user_id, status='Enrolled').first()
    if active_application:
        program_id = active_application.program_id
        program_course_info = ProgramCourse.query.filter_by(program_id=program_id, course_id=course_id).first()
        if program_course_info:
            target_semester = program_course_info.semester
        else:
            app.logger.warning(f"Course {course_id} not found in ProgramCourse mapping for program {program_id}. Semester set to 'Unknown'.")
    else:
        app.logger.warning(f"Could not find active application for user {user_id} to determine program context for manual enrollment.")


    # Check if already enrolled in this course for the current academic year
    existing_enrollment = CourseEnrollment.query.filter_by(
        user_id=user_id,
        course_id=course_id,
        academic_year=current_academic_year
    ).first()

    if existing_enrollment:
        return jsonify({'success': False, 'message': f'You are already enrolled in this course ({course.code}) for the academic year {current_academic_year}.'})

    # TODO: Add prerequisite checks before allowing enrollment
    # prereqs_met = check_prerequisites(user_id, course_id, current_academic_year)
    # if not prereqs_met:
    #     return jsonify({'success': False, 'message': 'Prerequisites not met.'})

    try:
        # Create new enrollment record
        enrollment = CourseEnrollment(
            user_id=user_id,
            course_id=course_id,
            program_id=program_id, # Store program context
            enrollment_date=datetime.now(UTC),
            status='Enrolled',
            semester=target_semester, # Store semester context
            academic_year=current_academic_year # Store academic year context
        )
        db.session.add(enrollment)
        db.session.commit()
        app.logger.info(f"User {user_id} manually enrolled in course {course_id} for {current_academic_year}.")
        flash(f'تم التسجيل بنجاح في مقرر {course.code}!', 'success') # RTL message
        return jsonify({'success': True, 'message': f'Successfully enrolled in {course.code}'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error manually enrolling user {user_id} in course {course_id}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'An error occurred during enrollment: {str(e)}'}), 500

@app.route('/admin/courses')
@login_required
def admin_courses():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
def admin_course_add():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        course = Course(
            code=request.form.get('code'),
            title=request.form.get('title'),
            description=request.form.get('description'),
            credits=int(request.form.get('credits')),
            prerequisites=request.form.get('prerequisites')
        )

        db.session.add(course)
        db.session.commit()

        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))

    return render_template('admin/course_add.html')

@app.route('/admin/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def admin_course_edit(course_id):
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        course.code = request.form.get('code')
        course.title = request.form.get('title')
        course.description = request.form.get('description')
        course.credits = int(request.form.get('credits'))
        course.prerequisites = request.form.get('prerequisites')
        course.is_active = 'is_active' in request.form

        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin_courses'))

    return render_template('admin/course_edit.html', course=course)

# ...existing code...

@app.route('/student/application/<int:application_id>/details')
@login_required
def student_application_details(application_id):
    """Return application details and documents for a specific application"""
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    # Get the application
    application = Application.query.get_or_404(application_id)

    # Ensure this application belongs to the current user
    if application.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': 'Access denied'
        }), 403

    # Get documents for this application
    documents = Document.query.filter_by(application_id=application.id).all()

    # Format documents for JSON
    formatted_documents = []
    for doc in documents:
        formatted_documents.append({
            'id': doc.id,
            'name': doc.name,
            'file_path': doc.file_path,
            'status': doc.status,
            'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M')
        })

    # Format application data
    application_data = {
        'id': application.id,
        'app_id': application.app_id,
        'program': application.program,
        'status': application.status,
        'payment_status': application.payment_status,
        'date': application.date_submitted.strftime('%Y-%m-%d')
    }

    # Get user info for document requirements
    user_info = {
        'nationality': current_user.nationality,
        'gender': 'male'  # Default as we don't store gender currently; you can update this if you have gender info
    }

    return jsonify({
        'success': True,
        'application': application_data,
        'documents': formatted_documents,
        'user_info': user_info
    })

# ...existing code...

# Add this context processor
@app.context_processor
def utility_processor():
    return {
        'now': datetime.now(UTC)
    }

from commands import init_app
init_app(app)

@app.route('/admin/students')
@login_required
def admin_students():
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    # Get students with university IDs
    student_ids = StudentID.query.all()

    students = []
    for student_id in student_ids:
        application = Application.query.get(student_id.application_id)
        if application:
            user = User.query.get(application.user_id)
            if user:
                students.append({
                    'id': user.id,
                    'student_id': student_id.student_id,
                    'name': user.full_name,
                    'program': application.program
                })

    return render_template('admin/students.html', students=students)

@app.route('/admin/student/<int:user_id>/courses')
@login_required
def admin_student_courses(user_id):
    if not current_user.is_admin():
        return redirect(url_for('student_dashboard'))

    # Get student
    student = User.query.get_or_404(user_id)

    # Get student's university ID
    student_id_obj = StudentID.query.join(Application).filter(
        Application.user_id == user_id
    ).first()

    if not student_id_obj:
        flash('Student has no university ID assigned.', 'warning')
        return redirect(url_for('admin_students'))

    # Get application and program
    application = student_id_obj.application
    program_name = application.program

    # Initialize courses list
    courses = []

    # Parse program name to get degree type and program name
    program_parts = program_name.split(' in ')
    if len(program_parts) == 2:
        degree_type = program_parts[0]
        prog_name = program_parts[1]

        # Find program in database
        program = Program.query.filter_by(
            name=prog_name,
            degree_type=degree_type
        ).first()

        if program:
            try:
                # Use raw SQL to get enrollments without relying on ORM columns
                sql = text("""
                    SELECT ce.id, ce.course_id, ce.grade, ce.grade_numeric, ce.status
                    FROM course_enrollments ce
                    WHERE ce.student_id = :student_id
                """)

                result = db.session.execute(sql, {"student_id": user_id})

                # Create a dict of enrollment data
                enrollments_dict = {}

                for row in result:
                    enrollments_dict[row[1]] = {
                        'id': row[0],
                        'grade': row[2],
                        'grade_numeric': row[3],
                        'status': row[4]
                    }

                # Get all program courses using ProgramCourse model
                program_course_relations = ProgramCourse.query.filter_by(
                    program_id=program.id
                ).all()

                # Build courses list with enrollment info
                for pc_relation in program_course_relations:
                    course = db.session.get(Course, pc_relation.course_id)

                    if course and course.is_active:
                        enrollment = enrollments_dict.get(course.id)

                        courses.append({
                            'course': course,
                            'semester': pc_relation.semester,
                            'enrollment_status': enrollment['status'] if enrollment else 'Not Enrolled',
                            'grade': enrollment['grade'] if enrollment else None,
                            'grade_numeric': enrollment['grade_numeric'] if enrollment else None,
                            'enrollment_id': enrollment['id'] if enrollment else None
                        })
            except Exception as e:
                print(f"Error in admin_student_courses: {str(e)}")
                # Continue with empty list if there's an error

    return render_template('admin/student_courses.html',
                         student=student,
                         student_id=student_id_obj.student_id,
                         program=program_name,
                         courses=courses)

@app.route('/admin/update_grade', methods=['POST'])
@login_required
def admin_update_grade():
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})

    enrollment_id = request.form.get('enrollment_id')
    grade = request.form.get('grade')

    # Debug print to server console
    print(f"Received grade update request: enrollment_id={enrollment_id}, grade={grade}")

    if not enrollment_id or not grade:
        return jsonify({'success': False, 'message': 'Missing required data'})

    try:
        # Get the enrollment record
        enrollment = CourseEnrollment.query.get_or_404(int(enrollment_id))

        # Convert grade to integer
        numerical_grade = int(float(grade))

        # Ensure grade is within valid range
        if numerical_grade < 0:
            numerical_grade = 0
        elif numerical_grade > 100:
            numerical_grade = 100

        # Map numerical grade to letter grade
        letter_grade = 'F'
        if numerical_grade >= 95:
            letter_grade = 'A+'
        elif numerical_grade >= 90:
            letter_grade = 'A'
        elif numerical_grade >= 85:
            letter_grade = 'A-'
        elif numerical_grade >= 80:
            letter_grade = 'B+'
        elif numerical_grade >= 75:
            letter_grade = 'B'
        elif numerical_grade >= 70:
            letter_grade = 'B-'
        elif numerical_grade >= 65:
            letter_grade = 'C+'
        elif numerical_grade >= 60:
            letter_grade = 'C'
        elif numerical_grade >= 55:
            letter_grade = 'C-'
        elif numerical_grade >= 50:
            letter_grade = 'D+'
        elif numerical_grade >= 45:
            letter_grade = 'D'

        # GPA value mapping
        gpa_map = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }

        # Update grade with letter representation
        enrollment.grade = letter_grade

        # Store numerical grade
        enrollment.grade_numeric = numerical_grade

        # Also set GPA value
        enrollment.gpa_value = gpa_map.get(letter_grade, 0.0)

        # Update status
        if numerical_grade < 50:
            enrollment.status = 'Failed'
        else:
            enrollment.status = 'Completed'

        db.session.commit()
        print(f"Grade updated successfully for enrollment ID: {enrollment_id}")

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error updating grade: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/program-info')
def api_program_info():
    degree_type = request.args.get('degree')
    program_name = request.args.get('name')

    app.logger.info(f"API Request - /api/program-info - degree: '{degree_type}', program_name: '{program_name}'") # Use app logger

    if not degree_type or not program_name:
        app.logger.warning("Missing parameters in /api/program-info request")
        return jsonify({'success': False, 'message': 'Missing parameters'})

    # Try to find the program using multiple strategies
    program = None
    search_strategies = [
        ("Direct match", lambda: Program.query.filter_by(name=program_name, degree_type=degree_type).first()),
        ("Case-insensitive match", lambda: Program.query.filter(Program.name.ilike(f"{program_name}"), Program.degree_type.ilike(f"{degree_type}")).first()),
        ("Partial name match", lambda: Program.query.filter(Program.name.ilike(f"%{program_name}%"), Program.degree_type.ilike(f"{degree_type}")).first()),
        ("Arabic name match", lambda: Program.query.filter(Program.arabic_name.ilike(f"%{program_name}%"), Program.degree_type.ilike(f"{degree_type}")).first())
    ]

    for strategy_name, search_func in search_strategies:
        program = search_func()
        if program:
            app.logger.info(f"Found program using strategy '{strategy_name}': ID={program.id}, Name={program.name}, Degree={program.degree_type}")
            break

    # Strategy 5: Try different program name variations (if still not found)
    if not program:
        app.logger.info("Program not found via standard strategies, trying variations...")
        # Handle special cases and common variations
        program_variations = {
            "Operations Research": ["Operations Research and Decision Support", "Operations Research", "بحوث العمليات"],
            "Statistical Quality Control": ["Statistical Quality Control & Quality Assurance", "Statistical Quality Control"],
            "Applied Statistics": ["Applied Statistics", "Statistics", "الإحصاء التطبيقي"]
            # Add more variations as needed
        }

        matched_variation = False
        for base_name, variations in program_variations.items():
            # Check if the requested name matches any variation (case-insensitive)
            if program_name.lower() in [v.lower() for v in variations]:
                app.logger.info(f"Requested name '{program_name}' matches variations for '{base_name}'. Searching...")
                for variant in variations:
                    program = Program.query.filter(
                        Program.name.ilike(f"%{variant}%"),
                        Program.degree_type.ilike(f"{degree_type}")
                    ).first()
                    if program:
                        app.logger.info(f"Found program using variation '{variant}': ID={program.id}, Name={program.name}")
                        matched_variation = True
                        break
                if matched_variation:
                    break
        if not matched_variation:
             app.logger.info("No matching variations found.")


    if not program:
        app.logger.warning(f"Program not found for degree_type='{degree_type}', name='{program_name}' after all strategies.")
        # Try to suggest similar programs
        similar_programs = Program.query.filter(
            Program.degree_type.ilike(f"{degree_type}")
        ).limit(3).all()
        suggestions = [p.name for p in similar_programs] if similar_programs else []
        return jsonify({
            'success': False,
            'message': 'Program not found',
            'suggestions': suggestions,
            'recommendation': 'Ensure program data is correctly populated in the database.'
        })

    # Found the program, now get its courses
    app.logger.info(f"Processing found program: ID={program.id}, Name={program.name}")

    # Get courses for program
    semester1_courses = []
    semester2_courses = []
    total_credits = 0

    # Use direct query with ProgramCourse to get all courses associated with this program
    program_courses = ProgramCourse.query.filter_by(program_id=program.id).all()
    app.logger.info(f"Found {len(program_courses)} course associations for program ID {program.id}")

    for program_course in program_courses:
        # Use db.session.get for potentially better performance with primary keys
        course = db.session.get(Course, program_course.course_id)
        if course:
            course_data = {
                'id': course.id,
                'code': course.code,
                'title': course.title,
                'credits': course.credits
            }

            if program_course.semester == 1:
                semester1_courses.append(course_data)
            elif program_course.semester == 2:
                semester2_courses.append(course_data)
            else:
                 app.logger.warning(f"Course association found with invalid semester ({program_course.semester}) for program ID {program.id}, course ID {course.id}")


            total_credits += course.credits
        else:
            app.logger.warning(f"Course with ID {program_course.course_id} referenced by ProgramCourse not found.")


    app.logger.info(f"Program {program.id}: Semester 1 courses: {len(semester1_courses)}, Semester 2 courses: {len(semester2_courses)}, Total Credits: {total_credits}")

    # Removed automatic population logic - this should be handled by a dedicated script/command
    # if not program_courses:
    #    app.logger.warning(f"No courses found for program {program.name} ({program.degree_type}). Manual population might be needed.")

    response_data = {
        'success': True,
        'program': {
            'id': program.id,
            'name': program.name,
            'degree_type': program.degree_type,
            'description': program.description,
            'arabic_name': program.arabic_name, # Include arabic name
            'semester1_courses': semester1_courses,
            'semester2_courses': semester2_courses,
            'total_credits': total_credits
        }
    }
    app.logger.info(f"Returning program info response for program ID {program.id}")

    return jsonify(response_data)

# ...existing code...

@app.route('/api/programs')
def api_programs():
    """Return available programs as JSON, optionally filtered"""
    try:
        # Get filters from query parameters
        degree_filter = request.args.get('degree_type') # Changed from 'degree' to 'degree_type'
        program_type_filter = request.args.get('type') # Keep this for potential future filtering

        app.logger.debug(f"API Request - /api/programs - degree_type='{degree_filter}', type='{program_type_filter}'")

        # Start with a base query
        query = Program.query

        # Apply filters if provided
        if degree_filter:
            # Filter by degree type (e.g., "Diploma", "Master", "PhD")
            query = query.filter(Program.degree_type.ilike(f"%{degree_filter}%"))
        if program_type_filter:
            # Filter by program type (e.g., "Academic", "Professional")
            if hasattr(Program, 'type'):
                query = query.filter(Program.type.ilike(f"%{program_type_filter}%"))
            else:
                 app.logger.warning("Program model does not have a 'type' attribute for filtering. Skipping type filter.")


        all_programs = query.order_by(Program.name).all() # Order by name within the degree type

        # Use a dictionary to ensure uniqueness by name+degree combination (though degree is filtered now)
        unique_programs = {}
        for program in all_programs:
            # Use a consistent key format
            key = f"{program.degree_type.strip()}_{program.name.strip()}"
            if key not in unique_programs:
                unique_programs[key] = {
                    'id': program.id,
                    'name': program.name,
                    'degree_type': program.degree_type, # Include degree_type here
                    'arabic_name': program.arabic_name
                    # 'type': program.type # Include type if it exists and is needed
                }

        programs_list = list(unique_programs.values())

        app.logger.info(f"Returning {len(programs_list)} unique programs based on filters (Degree Type: {degree_filter}, Type: {program_type_filter}).")
        return jsonify({
            'success': True,
            'programs': programs_list
        })
    except Exception as e:
        app.logger.error(f"Error fetching programs: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error fetching programs: {str(e)}'
        })

# --- ADD THE PDF ANALYSIS ENDPOINT ---
@app.route('/admin/analyze_transcript_pdf', methods=['POST'])
@login_required
def admin_analyze_transcript_pdf():
    """
    Reads a PDF file specified by path, sends it to Gemini for analysis
    against prerequisites, and returns the analysis text.
    """
    start_time = time.time()
    app.logger.info("Received request for /admin/analyze_transcript_pdf")

    if not current_user.is_admin():
        app.logger.warning("Access denied for non-admin user.")
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    # --- Get data from request ---
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data received.")
        # Expecting relative path like 'uploads/user_1_timestamp_transcript.pdf'
        relative_doc_path = data.get('document_path')
        application_id = data.get('application_id') # Optional, but good for logging

        if not relative_doc_path:
            raise ValueError("Missing 'document_path' in request.")

        app.logger.info(f"Analysis requested for doc path: {relative_doc_path}, app_id: {application_id}")

    except Exception as e:
        app.logger.error(f"Error parsing request data: {str(e)}")
        return jsonify({'success': False, 'message': f'Invalid request data: {str(e)}'}), 400

    # --- Construct full file path and check existence ---
    # Ensure UPLOAD_FOLDER is correctly configured and the path is relative to it
    # The path from JS is like '/static/uploads/filename.pdf', we need 'uploads/filename.pdf'
    # Or if JS sends 'uploads/filename.pdf', we need 'filename.pdf' relative to UPLOAD_FOLDER
    filename_part = None
    if relative_doc_path.startswith('/static/uploads/'):
        filename_part = relative_doc_path.split('/static/uploads/', 1)[1]
    elif relative_doc_path.startswith('uploads/'):
         filename_part = relative_doc_path.split('uploads/', 1)[1]
    else:
         # If it's just the filename, use it directly
         filename_part = relative_doc_path

    if not filename_part:
        app.logger.error(f"Could not extract filename from path: {relative_doc_path}")
        return jsonify({'success': False, 'message': 'Invalid document path format.'}), 400

    # Construct the full, absolute path
    full_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename_part))

    app.logger.info(f"Attempting to read PDF from absolute path: {full_file_path}")

    if not os.path.exists(full_file_path):
        app.logger.error(f"PDF file not found at path: {full_file_path}")
        app.logger.error(f"UPLOAD_FOLDER is configured as: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
        app.logger.error(f"Derived filename part: {filename_part}")
        return jsonify({'success': False, 'message': 'Transcript PDF file not found on server.'}), 404

    # --- Read and Encode PDF ---
    try:
        with open(full_file_path, "rb") as pdf_file:
            pdf_content_bytes = pdf_file.read()
        import base64 # Ensure base64 is imported
        pdf_base64 = base64.b64encode(pdf_content_bytes).decode('utf-8')
        app.logger.info(f"Successfully read and base64 encoded PDF: {len(pdf_base64)} chars")
    except Exception as e:
        app.logger.error(f"Error reading or encoding PDF file: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error processing PDF file: {str(e)}'}), 500

    # --- Prepare Prompt and Gemini API Call ---
    # Ensure GEMINI_API_KEY is configured in app.config or environment
    gemini_api_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key or gemini_api_key == "YOUR_FALLBACK_API_KEY_HERE": # Check against fallback
         app.logger.error("Gemini API Key is not configured in app.config or environment variables.")
         return jsonify({'success': False, 'message': 'AI analysis service is not configured.'}), 500
    else:
         app.logger.info("Using Gemini API Key.")


    # Use the latest stable or flash model that supports PDF input well
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"

    # Prerequisite courses text (exactly as provided in the prompt)
    prerequisite_courses_text = """
    First Semester (15 CHs)                    Second Semester (15 CHs)
    Course Code    Course Title    C.H    Course Code    Course Title    C.H
    SE101    Computer Systems Principles and Programming    3    
    SE106    Software Project Management    3
    SE102    Relational Database Systems    3    SE107    Web Design and Architecture    3
    SE103    The Software Development Process    3    SE108    Agile Software Development    3
    SE104    The User Interface Design    3    SE109    Programming in the Large    3
    SE105    Object-Oriented Software Development using UML    3    SE110    Project    3
"""

    # Construct the prompt
    prompt_text = f"""
You are a helpful academic advisor assistant for Cairo University's postgraduate programs. Attached is a PDF file containing a student's academic transcript.

Your task is to analyze the content of this PDF transcript and compare it with our prerequisite courses to determine if any complementary courses are needed for the Software Engineering postgraduate program.

Here are the prerequisite courses required:
{{ {prerequisite_courses_text} }}

Please perform the following analysis based only on the content within the provided PDF file:

1.  **Identify Courses:** List all *completed* courses mentioned in the transcript PDF, including course codes and names if available. Ignore courses listed as 'in progress' or similar statuses.
2.  **Prerequisite Check:** Compare the identified completed courses against the prerequisite list (SE101 to SE110). Clearly state which prerequisites appear to be met based on the transcript content. Use course codes for matching where possible.
3.  **Missing Prerequisites:** Explicitly list any prerequisite courses (SE101 to SE110) that are *not found* as completed in the transcript PDF.
4.  **Conclusion:** Provide a brief, clear summary stating whether the student appears to meet all prerequisites based *solely* on this transcript PDF, or if prerequisites seem to be missing.

**Important Formatting Instructions:**
*   Use Markdown for formatting.
*   Use clear headings (e.g., `## Identified Courses`, `## Prerequisite Status`, `## Missing Prerequisites`, `## Conclusion`).
*   Use bullet points for lists (`* ` or `- `).
*   Be concise and focus *only* on the requested analysis based on the PDF. Do not add greetings, apologies, or conversational filler.
"""

    request_payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_base64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
          "temperature": 0.3,
          "maxOutputTokens": 2048
        },
        "safetySettings": [ # Add safety settings
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]
    }

    headers = {'Content-Type': 'application/json'}

    # --- Make the API Call ---
    try:
        api_call_start = time.time()
        # Ensure requests library is imported: import requests
        response = requests.post(gemini_url, headers=headers, json=request_payload, timeout=120) # Increased timeout
        api_call_end = time.time()
        app.logger.info(f"Gemini API call took {api_call_end - api_call_start:.2f} seconds. Status: {response.status_code}")

        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        response_data = response.json()
        app.logger.debug(f"Gemini Raw Response: {json.dumps(response_data)[:500]}...") # Log part of the raw response

        # --- Extract Text and Handle Potential Errors ---
        analysis_text = None
        finish_reason = None
        safety_ratings = None

        if 'candidates' in response_data and response_data['candidates']:
            candidate = response_data['candidates'][0]
            finish_reason = candidate.get('finishReason')
            safety_ratings = candidate.get('safetyRatings')

            if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
                analysis_text = candidate['content']['parts'][0].get('text', '')

        elif 'promptFeedback' in response_data and response_data['promptFeedback'].get('blockReason'):
             block_reason = response_data['promptFeedback']['blockReason']
             safety_ratings = response_data['promptFeedback'].get('safetyRatings', [])
             app.logger.warning(f"Gemini prompt blocked. Reason: {block_reason}, Ratings: {safety_ratings}")
             raise ValueError(f"Analysis request blocked by AI service. Reason: {block_reason}")

        # --- Process the result or error ---
        if analysis_text is not None:
            if finish_reason == 'SAFETY':
                 app.logger.warning(f"Gemini response potentially blocked due to safety. Finish Reason: {finish_reason}, Ratings: {safety_ratings}")
                 raise ValueError("Analysis may be incomplete or blocked due to safety settings. Please check the document content.")
            elif finish_reason and finish_reason != 'STOP':
                 app.logger.warning(f"Gemini generation finished unexpectedly. Reason: {finish_reason}")

            if not analysis_text.strip():
                 app.logger.warning("Gemini response received but text part is empty.")
                 raise ValueError("AI analysis returned an empty result.")

            app.logger.info("Successfully received analysis from Gemini.")
            end_time = time.time()
            app.logger.info(f"Total analysis request processed in {end_time - start_time:.2f} seconds.")

            return jsonify({
                'success': True,
                'analysis_text': analysis_text.strip()
            })
        else:
             app.logger.error(f"Malformed or empty Gemini response. Response: {response_data}")
             raise ValueError("Received an incomplete or unexpected response from the AI service.")


    except requests.exceptions.HTTPError as e:
        error_message = f"AI service returned an error: {e}"
        try:
            error_details = response.json().get('error', {})
            gemini_error = error_details.get('message', str(e))
            error_message = f"AI service error: {gemini_error}"
            app.logger.error(f"Gemini API HTTP Error Details: {error_details}")
        except:
            app.logger.error(f"Gemini API HTTP Error (non-JSON or parse failed): {response.text}")
        return jsonify({'success': False, 'message': error_message}), response.status_code if response is not None else 500

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Failed to communicate with AI service: {str(e)}'}), 503 # Service Unavailable
    except ValueError as e:
         app.logger.error(f"Value error during Gemini processing: {str(e)}")
         return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error during AI analysis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}), 500

# MOVED: admin_application_details route moved here, before app.run()
@app.route('/admin/application/<int:application_id>/details', methods=['GET'])
@login_required
def admin_application_details(application_id):
    """Return application details and documents for admin view"""
    app.logger.debug(f"Accessing admin_application_details for ID: {application_id} with method: {request.method}")
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    try:
        # Get the application
        application = Application.query.get_or_404(application_id)

        # Get documents for this application
        documents = Document.query.filter_by(application_id=application.id).all()

        # Format documents for JSON
        formatted_documents = []
        for doc in documents:
            formatted_documents.append({
                'id': doc.id,
                'name': doc.name,
                'file_path': doc.file_path,
                'status': doc.status,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M')
            })

        # Format application data with user information
        user = application.user
        application_data = {
            'id': application.id,
            'app_id': application.app_id,
            'applicant': user.full_name,
            'email': user.email,
            'phone': user.phone or 'Not provided',
            'program': application.program,
            'status': application.status,
            'payment_status': application.payment_status,
            'date': application.date_submitted.strftime('%Y-%m-%d')
        }

        return jsonify({
            'success': True,
            'application': application_data,
            'documents': formatted_documents
        })
    except Exception as e:
        app.logger.error(f"Error retrieving application details for ID {application_id}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error retrieving application details: {str(e)}'
        }), 500


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Check and add missing columns
        try:
            print("Checking for missing columns...")
            # Use raw SQL to check if columns exist and add if missing
            
            # Check course_enrollments table
            result_ce = db.session.execute(text("PRAGMA table_info(course_enrollments)")).fetchall()
            columns_ce = [row[1] for row in result_ce]
            
            if 'gpa_value' not in columns_ce:
                print("Adding missing gpa_value column to course_enrollments...")
                db.session.execute(text("ALTER TABLE course_enrollments ADD COLUMN gpa_value FLOAT"))
                db.session.commit()
                print("Column gpa_value added successfully!")
            else:
                print("Column gpa_value already exists in course_enrollments.")

            if 'program_id' not in columns_ce:
                print("Adding missing program_id column to course_enrollments...")
                # Add the foreign key constraint as well
                db.session.execute(text("ALTER TABLE course_enrollments ADD COLUMN program_id INTEGER REFERENCES programs(id)"))
                db.session.commit()
                print("Column program_id added successfully!")
            else:
                print("Column program_id already exists in course_enrollments.")

            # --- ADD ACADEMIC YEAR CHECK ---
            if 'academic_year' not in columns_ce:
                print("Adding missing academic_year column to course_enrollments...")
                # Assuming VARCHAR(20) similar to application table
                db.session.execute(text("ALTER TABLE course_enrollments ADD COLUMN academic_year VARCHAR(20)"))
                db.session.commit()
                print("Column academic_year added successfully!")
            else:
                print("Column academic_year already exists in course_enrollments.")
            # --- END OF ACADEMIC YEAR CHECK ---

            # --- ADD SEMESTER CHECK ---
            if 'semester' not in columns_ce:
                print("Adding missing semester column to course_enrollments...")
                # Assuming VARCHAR(50) to match ProgramCourse.semester or adjust as needed
                db.session.execute(text("ALTER TABLE course_enrollments ADD COLUMN semester VARCHAR(50)"))
                db.session.commit()
                print("Column semester added successfully!")
            else:
                print("Column semester already exists in course_enrollments.")
            # --- END OF SEMESTER CHECK ---

            # Check programs table
            result_prog = db.session.execute(text("PRAGMA table_info(programs)")).fetchall()
            columns_prog = [row[1] for row in result_prog]
            if 'arabic_name' not in columns_prog:
                print("Adding missing arabic_name column to programs...")
                db.session.execute(text("ALTER TABLE programs ADD COLUMN arabic_name TEXT"))
                db.session.commit()
                print("Column arabic_name added successfully!")
            else:
                 print("Column arabic_name already exists in programs.")

            if 'arabic_description' not in columns_prog:
                print("Adding missing arabic_description column to programs...")
                db.session.execute(text("ALTER TABLE programs ADD COLUMN arabic_description TEXT"))
                db.session.commit()
                print("Column arabic_description added successfully!")
            else:
                 print("Column arabic_description already exists in programs.")
                 
            # Add check for 'type' column in programs table
            if 'type' not in columns_prog:
                print("Adding missing type column to programs...")
                db.session.execute(text("ALTER TABLE programs ADD COLUMN type VARCHAR(50)"))
                db.session.commit()
                print("Column type added successfully!")
            else:
                print("Column type already exists in programs.")

            # Check application table
            result_app = db.session.execute(text("PRAGMA table_info(application)")).fetchall()
            columns_app = [row[1] for row in result_app]
            if 'academic_year' not in columns_app:
                print("Adding missing academic_year column to application...")
                db.session.execute(text("ALTER TABLE application ADD COLUMN academic_year VARCHAR(20)"))
                db.session.commit()
                print("Column academic_year added successfully!")
            else:
                print("Column academic_year already exists in application.")

            if 'semester' not in columns_app:
                print("Adding missing semester column to application...")
                db.session.execute(text("ALTER TABLE application ADD COLUMN semester VARCHAR(10)"))
                db.session.commit()
                print("Column semester added successfully!")
            else:
                print("Column semester already exists in application.")

            if 'program_type' not in columns_app:
                print("Adding missing program_type column to application...")
                db.session.execute(text("ALTER TABLE application ADD COLUMN program_type VARCHAR(50)"))
                db.session.commit()
                print("Column program_type added successfully!")
            else:
                print("Column program_type already exists in application.")

        except Exception as e:
            print(f"Error checking/adding columns: {str(e)}")
            traceback.print_exc()
            # It's safer to rollback in case of error during schema modification
            db.session.rollback()


      

    app.run(debug=True)


