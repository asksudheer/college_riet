from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.staff import bp
from app.models import *
from app import db
from datetime import datetime, date

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied. Staff/Principal access required.')
        return redirect(url_for('main.index'))
    
    # Get dashboard statistics
    total_students = Student.query.count()
    total_staff = Staff.query.count()
    pending_fee_approvals = FeePayment.query.filter_by(status='pending').count()
    today_events = Event.query.filter_by(event_date=date.today()).count()
    
    return render_template('staff/dashboard.html', 
                         total_students=total_students,
                         total_staff=total_staff,
                         pending_fee_approvals=pending_fee_approvals,
                         today_events=today_events)

# Examination Management
@bp.route('/examinations')
@login_required
def examinations():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    exams = Examination.query.all()
    return render_template('staff/examinations.html', exams=exams)

@bp.route('/examinations/add', methods=['GET', 'POST'])
@login_required
def add_examination():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        exam = Examination(
            name=request.form['name'],
            subject=request.form['subject'],
            course=request.form['course'],
            year=int(request.form['year']),
            semester=int(request.form['semester']),
            exam_date=datetime.strptime(request.form['exam_date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(request.form['start_time'], '%H:%M').time(),
            duration_minutes=int(request.form['duration_minutes']),
            max_marks=int(request.form['max_marks']),
            created_by=current_user.staff.id
        )
        db.session.add(exam)
        db.session.commit()
        flash('Examination added successfully!')
        return redirect(url_for('staff.examinations'))
    
    return render_template('staff/add_examination.html')

# Fee Management
@bp.route('/fee-structure')
@login_required
def fee_structure():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    fees = FeeStructure.query.all()
    return render_template('staff/fee_structure.html', fees=fees)

@bp.route('/fee-payments')
@login_required
def fee_payments():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    payments = FeePayment.query.all()
    return render_template('staff/fee_payments.html', payments=payments)

@bp.route('/approve-payment/<int:payment_id>/<int:level>')
@login_required
def approve_payment(payment_id, level):
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    payment = FeePayment.query.get_or_404(payment_id)
    
    if level == 1:
        payment.level1_approver = current_user.staff.id
        payment.level1_approval_date = datetime.utcnow()
        payment.status = 'level1_approved'
    elif level == 2 and current_user.role == 'principal':
        payment.level2_approver = current_user.staff.id
        payment.level2_approval_date = datetime.utcnow()
        payment.status = 'approved'
    
    db.session.commit()
    flash(f'Payment approved at level {level}!')
    return redirect(url_for('staff.fee_payments'))

# Transportation Management
@bp.route('/transportation')
@login_required
def transportation():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    routes = BusRoute.query.all()
    buses = Bus.query.all()
    return render_template('staff/transportation.html', routes=routes, buses=buses)

@bp.route('/bus-routes/add', methods=['GET', 'POST'])
@login_required
def add_bus_route():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        route = BusRoute(
            route_name=request.form['route_name'],
            route_number=request.form['route_number'],
            starting_point=request.form['starting_point'],
            ending_point=request.form['ending_point'],
            total_distance=float(request.form['total_distance']),
            estimated_time=int(request.form['estimated_time']),
            stops=request.form['stops'],
            monthly_fee=float(request.form['monthly_fee']),
            term_fee=float(request.form['term_fee'])
        )
        db.session.add(route)
        db.session.commit()
        flash('Bus route added successfully!')
        return redirect(url_for('staff.transportation'))
    
    return render_template('staff/add_bus_route.html')

# Attendance Management
@bp.route('/attendance')
@login_required
def attendance():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    students = Student.query.all()
    return render_template('staff/attendance.html', students=students)

@bp.route('/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role not in ['staff', 'principal']:
        return jsonify({'error': 'Access denied'}), 403
    
    student_id = request.json['student_id']
    subject = request.json['subject']
    status = request.json['status']
    attendance_date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
    
    # Check if attendance already marked for this date
    existing = Attendance.query.filter_by(
        student_id=student_id,
        subject=subject,
        date=attendance_date
    ).first()
    
    if existing:
        existing.status = status
        existing.marked_by = current_user.staff.id
        existing.marked_at = datetime.utcnow()
    else:
        attendance = Attendance(
            student_id=student_id,
            subject=subject,
            date=attendance_date,
            status=status,
            marked_by=current_user.staff.id
        )
        db.session.add(attendance)
    
    db.session.commit()
    return jsonify({'success': True})

# Event Management
@bp.route('/events')
@login_required
def events():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    events = Event.query.all()
    return render_template('staff/events.html', events=events)

@bp.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        event = Event(
            title=request.form['title'],
            description=request.form['description'],
            event_date=datetime.strptime(request.form['event_date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(request.form['start_time'], '%H:%M').time() if request.form['start_time'] else None,
            end_time=datetime.strptime(request.form['end_time'], '%H:%M').time() if request.form['end_time'] else None,
            venue=request.form['venue'],
            event_type=request.form['event_type'],
            target_audience=request.form['target_audience'],
            created_by=current_user.staff.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!')
        return redirect(url_for('staff.events'))
    
    return render_template('staff/add_event.html')

# Library Management
@bp.route('/library')
@login_required
def library():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    resources = LibraryResource.query.all()
    return render_template('staff/library.html', resources=resources)

@bp.route('/library/add-resource', methods=['GET', 'POST'])
@login_required
def add_library_resource():
    if current_user.role not in ['staff', 'principal']:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        resource = LibraryResource(
            title=request.form['title'],
            subject=request.form['subject'],
            course=request.form['course'],
            year=int(request.form['year']) if request.form['year'] else None,
            semester=int(request.form['semester']) if request.form['semester'] else None,
            resource_type=request.form['resource_type'],
            author=request.form['author'],
            description=request.form['description'],
            added_by=current_user.staff.id
        )
        db.session.add(resource)
        db.session.commit()
        flash('Library resource added successfully!')
        return redirect(url_for('staff.library'))
    
    return render_template('staff/add_library_resource.html')
