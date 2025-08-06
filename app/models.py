from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'staff', 'principal'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    
    user = db.relationship('User', backref=db.backref('student', uselist=False))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    hire_date = db.Column(db.Date, nullable=False)
    
    user = db.relationship('User', backref=db.backref('staff', uselist=False))

class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    marks_obtained = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(5))
    remarks = db.Column(db.Text)
    
    examination = db.relationship('Examination', backref='results')
    student = db.relationship('Student', backref='exam_results')

class FeeStructure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    tuition_fee = db.Column(db.Float, nullable=False)
    lab_fee = db.Column(db.Float, default=0)
    library_fee = db.Column(db.Float, default=0)
    sports_fee = db.Column(db.Float, default=0)
    other_fees = db.Column(db.Float, default=0)
    total_fee = db.Column(db.Float, nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FeePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structure.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, level1_approved, approved, rejected
    level1_approver = db.Column(db.Integer, db.ForeignKey('staff.id'))
    level2_approver = db.Column(db.Integer, db.ForeignKey('staff.id'))
    level1_approval_date = db.Column(db.DateTime)
    level2_approval_date = db.Column(db.DateTime)
    remarks = db.Column(db.Text)
    
    student = db.relationship('Student', backref='fee_payments')
    fee_structure = db.relationship('FeeStructure', backref='payments')

class BusRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    route_number = db.Column(db.String(20), unique=True, nullable=False)
    starting_point = db.Column(db.String(200), nullable=False)
    ending_point = db.Column(db.String(200), nullable=False)
    total_distance = db.Column(db.Float, nullable=False)
    estimated_time = db.Column(db.Integer, nullable=False)  # in minutes
    stops = db.Column(db.Text)  # JSON string of stops
    monthly_fee = db.Column(db.Float, nullable=False)
    term_fee = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('bus_route.id'), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    driver_phone = db.Column(db.String(15), nullable=False)
    conductor_name = db.Column(db.String(100))
    conductor_phone = db.Column(db.String(15))
    capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='available')  # available, on_route, maintenance
    
    route = db.relationship('BusRoute', backref='buses')

class BusSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('bus_route.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    pickup_stop = db.Column(db.String(200), nullable=False)
    
    student = db.relationship('Student', backref='bus_subscriptions')
    route = db.relationship('BusRoute', backref='subscriptions')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # present, absent, late
    marked_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    remarks = db.Column(db.Text)
    
    student = db.relationship('Student', backref='attendance_records')
    staff = db.relationship('Staff', backref='marked_attendance')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    venue = db.Column(db.String(200))
    event_type = db.Column(db.String(50), nullable=False)  # academic, cultural, sports, etc.
    target_audience = db.Column(db.String(100))  # all, specific_course, specific_year
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    creator = db.relationship('Staff', backref='created_events')

class LibraryResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    resource_type = db.Column(db.String(50), nullable=False)  # book, exam_paper, notes, etc.
    file_path = db.Column(db.String(500))
    author = db.Column(db.String(200))
    publication_date = db.Column(db.Date)
    description = db.Column(db.Text)
    added_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)
    
    added_by_staff = db.relationship('Staff', backref='added_resources')

class LibraryAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('library_resource.id'), nullable=False)
    access_date = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=1)
    
    student = db.relationship('Student', backref='library_access')
    resource = db.relationship('LibraryResource', backref='access_logs')
