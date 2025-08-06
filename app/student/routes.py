from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.student import bp
from app.models import Student, Attendance, Event, LibraryResource, LibraryAccess, ExamResult, BusSubscription, BusRoute
from app import db
from datetime import datetime, date
from sqlalchemy import func

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Access denied. Student access required.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    if not student:
        flash('Student profile not found.')
        return redirect(url_for('main.index'))
    
    # Get dashboard statistics
    total_attendance = Attendance.query.filter_by(student_id=student.id).count()
    present_count = Attendance.query.filter_by(student_id=student.id, status='present').count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    upcoming_events = Event.query.filter(Event.event_date >= date.today()).limit(5).all()
    recent_results = ExamResult.query.filter_by(student_id=student.id).limit(5).all()
    
    return render_template('student/dashboard.html',
                         student=student,
                         attendance_percentage=attendance_percentage,
                         upcoming_events=upcoming_events,
                         recent_results=recent_results)

@bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    return render_template('student/profile.html', student=student)

@bp.route('/attendance')
@login_required
def attendance():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    attendance_records = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).all()
    
    # Calculate subject-wise attendance
    subject_attendance = {}
    for record in attendance_records:
        if record.subject not in subject_attendance:
            subject_attendance[record.subject] = {'total': 0, 'present': 0}
        subject_attendance[record.subject]['total'] += 1
        if record.status == 'present':
            subject_attendance[record.subject]['present'] += 1
    
    # Calculate percentages
    for subject in subject_attendance:
        total = subject_attendance[subject]['total']
        present = subject_attendance[subject]['present']
        subject_attendance[subject]['percentage'] = (present / total * 100) if total > 0 else 0
    
    return render_template('student/attendance.html',
                         attendance_records=attendance_records,
                         subject_attendance=subject_attendance)

@bp.route('/academics')
@login_required
def academics():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    exam_results = ExamResult.query.filter_by(student_id=student.id).join(
        ExamResult.examination
    ).order_by('examination.exam_date desc').all()
    
    # Calculate semester-wise performance
    semester_performance = {}
    for result in exam_results:
        semester = f"Year {result.examination.year} - Semester {result.examination.semester}"
        if semester not in semester_performance:
            semester_performance[semester] = {'total_marks': 0, 'obtained_marks': 0, 'subjects': 0}
        
        semester_performance[semester]['total_marks'] += result.examination.max_marks
        semester_performance[semester]['obtained_marks'] += result.marks_obtained
        semester_performance[semester]['subjects'] += 1
    
    # Calculate percentages
    for semester in semester_performance:
        total = semester_performance[semester]['total_marks']
        obtained = semester_performance[semester]['obtained_marks']
        semester_performance[semester]['percentage'] = (obtained / total * 100) if total > 0 else 0
    
    return render_template('student/academics.html',
                         exam_results=exam_results,
                         semester_performance=semester_performance,
                         student=student)

@bp.route('/library')
@login_required
def library():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    subject = request.args.get('subject', '')
    resource_type = request.args.get('type', '')
    
    # Build query based on filters
    query = LibraryResource.query.filter_by(is_available=True)
    
    if subject:
        query = query.filter(LibraryResource.subject.ilike(f'%{subject}%'))
    if resource_type:
        query = query.filter_by(resource_type=resource_type)
    
    # Filter by student's course and year
    query = query.filter(
        (LibraryResource.course == student.course) |
        (LibraryResource.course == 'all')
    ).filter(
        (LibraryResource.year == student.year) |
        (LibraryResource.year == None)
    )
    
    resources = query.all()
    
    # Get unique subjects and resource types for filters
    subjects = db.session.query(LibraryResource.subject).distinct().all()
    resource_types = db.session.query(LibraryResource.resource_type).distinct().all()
    
    return render_template('student/library.html',
                         resources=resources,
                         subjects=[s[0] for s in subjects],
                         resource_types=[r[0] for r in resource_types],
                         current_subject=subject,
                         current_type=resource_type)

@bp.route('/library/access/<int:resource_id>')
@login_required
def access_resource(resource_id):
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    resource = LibraryResource.query.get_or_404(resource_id)
    
    # Log the access
    access_log = LibraryAccess.query.filter_by(
        student_id=student.id,
        resource_id=resource_id
    ).first()
    
    if access_log:
        access_log.download_count += 1
        access_log.access_date = datetime.utcnow()
    else:
        access_log = LibraryAccess(
            student_id=student.id,
            resource_id=resource_id
        )
        db.session.add(access_log)
    
    db.session.commit()
    
    # In a real application, you would serve the actual file here
    flash(f'Accessing resource: {resource.title}')
    return redirect(url_for('student.library'))

@bp.route('/events')
@login_required
def events():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    
    # Get current and upcoming events
    current_events = Event.query.filter(
        Event.event_date >= date.today(),
        Event.is_active == True
    ).filter(
        (Event.target_audience == 'all') |
        (Event.target_audience.ilike(f'%{student.course}%')) |
        (Event.target_audience.ilike(f'%year_{student.year}%'))
    ).order_by(Event.event_date.asc()).all()
    
    # Get past events for reference
    past_events = Event.query.filter(
        Event.event_date < date.today(),
        Event.is_active == True
    ).filter(
        (Event.target_audience == 'all') |
        (Event.target_audience.ilike(f'%{student.course}%')) |
        (Event.target_audience.ilike(f'%year_{student.year}%'))
    ).order_by(Event.event_date.desc()).limit(10).all()
    
    return render_template('student/events.html',
                         current_events=current_events,
                         past_events=past_events)

@bp.route('/transportation')
@login_required
def transportation():
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    student = current_user.student
    
    # Get student's current bus subscriptions
    subscriptions = BusSubscription.query.filter_by(
        student_id=student.id,
        is_active=True
    ).all()
    
    # Get available routes
    available_routes = BusRoute.query.filter_by(is_active=True).all()
    
    return render_template('student/transportation.html',
                         subscriptions=subscriptions,
                         available_routes=available_routes)

@bp.route('/api/attendance-chart')
@login_required
def attendance_chart_data():
    if current_user.role != 'student':
        return jsonify({'error': 'Access denied'}), 403
    
    student = current_user.student
    
    # Get monthly attendance data for the last 6 months
    attendance_data = db.session.query(
        func.strftime('%Y-%m', Attendance.date).label('month'),
        func.count(Attendance.id).label('total'),
        func.sum(func.case([(Attendance.status == 'present', 1)], else_=0)).label('present')
    ).filter_by(student_id=student.id).group_by(
        func.strftime('%Y-%m', Attendance.date)
    ).order_by('month desc').limit(6).all()
    
    chart_data = {
        'months': [row.month for row in reversed(attendance_data)],
        'percentages': [
            (row.present / row.total * 100) if row.total > 0 else 0 
            for row in reversed(attendance_data)
        ]
    }
    
    return jsonify(chart_data)
