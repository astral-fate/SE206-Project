# Make sure these imports are at the very top of the file
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
import os
import requests
import traceback
import json
import sys

# Try to import PyMuPDF but provide a fallback if it's not available
try:
    import fitz  # PyMuPDF for PDF text extraction
    PYMUPDF_AVAILABLE = True
except ImportError:
    print("WARNING: PyMuPDF not installed. PDF text extraction will not work.")
    print("Install with: pip install PyMuPDF")
    PYMUPDF_AVAILABLE = False

# In your route handler for new tickets
@app.route('/student/support/new', methods=['GET', 'POST'])
@login_required
def student_new_ticket():
    form = TicketForm()  # Make sure this form is properly initialized
    
    if form.validate_on_submit():
        # Process the form submission
        # Add your form processing logic here
        pass
        
    return render_template('student/new_ticket.html', form=form)

# Add this route to your Flask application

import os
import json
import requests
from flask import request, jsonify
import fitz  # PyMuPDF for PDF text extraction

# Add this to your existing import section
# pip install PyMuPDF google-generativeai

# Add these imports at the top of the file with other imports
import requests
try:
    import fitz  # PyMuPDF for PDF text extraction
    PYMUPDF_AVAILABLE = True
except ImportError:
    print("WARNING: PyMuPDF not installed. PDF text extraction will not work.")
    print("Install with: pip install PyMuPDF")
    PYMUPDF_AVAILABLE = False



# MOVED: admin_application_details route moved here, before app.run()
@app.route('/admin/application/<int:application_id>/details', methods=['GET'])
@login_required
def admin_application_details(application_id):
    # ... existing admin_application_details code ...
    pass # Keep existing code here

# Add this new route for sending notes
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

        # Generate a unique ticket ID
        ticket_count = Ticket.query.count() + 1
        ticket_id_str = f"NOTE-{ticket_count:03d}"

        # Create a new ticket for the note
        new_ticket = Ticket(
            ticket_id=ticket_id_str,
            user_id=student.id,
            subject=subject,
            status='Open' # Or maybe 'Info' if you want to differentiate notes
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


if __name__ == '__main__':
    with app.app_context():
        # Database initialization code
        # ...
        pass
    
    print("Starting Flask application...")
    app.run(debug=True)