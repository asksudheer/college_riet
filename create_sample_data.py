from app import create_app, db
from app.models import *
from datetime import datetime, date, timedelta
import json

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create users
        print("Creating users...")
        
        # Principal user
        principal_user = User(username='principal', email='principal@college.edu', role='principal')
        principal_user.set_password('principal123')
        db.session.add(principal_user)
        
        # Staff user
        staff_user = User(username='staff1', email='staff1@college.edu', role='staff')
        staff_user.set_password('staff123')
        db.session.add(staff_user)
        
        # Student users
        student1_user = User(username='student1', email='student1@college.edu', role='student')
        student1_user.set_password('student123')
        db.session.add(student1_user)
        
        student2_user = User(username='student2', email='student2@college.edu', role='student')
        student2_user.set_password('student123')
        db.session.add(student2_user)
        
        db.session.commit()
        
        # Create staff profiles
        print("Creating staff profiles...")
        principal_staff = Staff(
            user_id=principal_user.id,
            employee_id='EMP001',
            first_name='Dr. John',
            last_name='Smith',
            department='Administration',
            designation='Principal',
            phone='+1234567890',
            address='123 College Street',
            hire_date=date(2020, 1, 1)
        )
        db.session.add(principal_staff)
        
        staff1_profile = Staff(
            user_id=staff_user.id,
            employee_id='EMP002',
            first_name='Prof. Jane',
            last_name='Doe',
            department='Computer Science',
            designation='Associate Professor',
            phone='+1234567891',
            address='456 Faculty Avenue',
            hire_date=date(2021, 8, 15)
        )
        db.session.add(staff1_profile)
        
        # Create student profiles
        print("Creating student profiles...")
        student1_profile = Student(
            user_id=student1_user.id,
            student_id='STU2023001',
            first_name='Alice',
            last_name='Johnson',
            date_of_birth=date(2003, 5, 15),
            gender='Female',
            phone='+1234567892',
            address='789 Student Lane',
            course='Computer Science',
            year=2,
            semester=3,
            admission_date=date(2023, 8, 1)
        )
        db.session.add(student1_profile)
        
        student2_profile = Student(
            user_id=student2_user.id,
            student_id='STU2023002',
            first_name='Bob',
            last_name='Williams',
            date_of_birth=date(2003, 8, 22),
            gender='Male',
            phone='+1234567893',
            address='321 Campus Road',
            course='Computer Science',
            year=2,
            semester=3,
            admission_date=date(2023, 8, 1)
        )
        db.session.add(student2_profile)
        
        db.session.commit()
        
        # Create fee structure
        print("Creating fee structure...")
        fee_structure = FeeStructure(
            course='Computer Science',
            year=2,
            semester=3,
            tuition_fee=5000.0,
            lab_fee=500.0,
            library_fee=200.0,
            sports_fee=300.0,
            other_fees=100.0,
            total_fee=6100.0,
            academic_year='2023-24'
        )
        db.session.add(fee_structure)
        
        db.session.commit()
        
        # Create examinations
        print("Creating examinations...")
        exam1 = Examination(
            name='Mid-Term Examination',
            subject='Database Systems',
            course='Computer Science',
            year=2,
            semester=3,
            exam_date=date.today() + timedelta(days=30),
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            duration_minutes=180,
            max_marks=100,
            created_by=staff1_profile.id
        )
        db.session.add(exam1)
        
        exam2 = Examination(
            name='Mid-Term Examination',
            subject='Web Development',
            course='Computer Science',
            year=2,
            semester=3,
            exam_date=date.today() + timedelta(days=32),
            start_time=datetime.strptime('14:00', '%H:%M').time(),
            duration_minutes=180,
            max_marks=100,
            created_by=staff1_profile.id
        )
        db.session.add(exam2)
        
        db.session.commit()
        
        # Create bus routes
        print("Creating transportation...")
        route1 = BusRoute(
            route_name='City Center Route',
            route_number='R001',
            starting_point='City Center',
            ending_point='College Campus',
            total_distance=15.5,
            estimated_time=45,
            stops=json.dumps(['City Center', 'Mall Junction', 'Park Street', 'University Gate', 'College Campus']),
            monthly_fee=150.0,
            term_fee=450.0,
            is_active=True
        )
        db.session.add(route1)
        
        route2 = BusRoute(
            route_name='Suburban Route',
            route_number='R002',
            starting_point='Suburbia',
            ending_point='College Campus',
            total_distance=22.0,
            estimated_time=60,
            stops=json.dumps(['Suburbia', 'Metro Station', 'Shopping Complex', 'Hospital Junction', 'College Campus']),
            monthly_fee=200.0,
            term_fee=600.0,
            is_active=True
        )
        db.session.add(route2)
        
        db.session.commit()
        
        # Create buses
        bus1 = Bus(
            bus_number='CL-001',
            route_id=route1.id,
            driver_name='Mike Johnson',
            driver_phone='+1234567894',
            conductor_name='Sarah Davis',
            conductor_phone='+1234567895',
            capacity=50,
            current_occupancy=25,
            status='available'
        )
        db.session.add(bus1)
        
        bus2 = Bus(
            bus_number='CL-002',
            route_id=route2.id,
            driver_name='David Brown',
            driver_phone='+1234567896',
            conductor_name='Lisa Wilson',
            conductor_phone='+1234567897',
            capacity=45,
            current_occupancy=30,
            status='available'
        )
        db.session.add(bus2)
        
        db.session.commit()
        
        # Create attendance records
        print("Creating attendance records...")
        for i in range(1, 31):  # Last 30 days
            attendance_date = date.today() - timedelta(days=i)
            
            # Student 1 attendance (85% attendance)
            if i % 7 != 0:  # Miss one day per week
                attendance1 = Attendance(
                    student_id=student1_profile.id,
                    subject='Database Systems',
                    date=attendance_date,
                    status='present',
                    marked_by=staff1_profile.id
                )
                db.session.add(attendance1)
                
                attendance2 = Attendance(
                    student_id=student1_profile.id,
                    subject='Web Development',
                    date=attendance_date,
                    status='present',
                    marked_by=staff1_profile.id
                )
                db.session.add(attendance2)
            
            # Student 2 attendance (92% attendance)
            if i % 12 != 0:  # Miss fewer days
                attendance3 = Attendance(
                    student_id=student2_profile.id,
                    subject='Database Systems',
                    date=attendance_date,
                    status='present',
                    marked_by=staff1_profile.id
                )
                db.session.add(attendance3)
                
                attendance4 = Attendance(
                    student_id=student2_profile.id,
                    subject='Web Development',
                    date=attendance_date,
                    status='present',
                    marked_by=staff1_profile.id
                )
                db.session.add(attendance4)
        
        db.session.commit()
        
        # Create events
        print("Creating events...")
        event1 = Event(
            title='Annual Sports Day',
            description='College annual sports competition with various indoor and outdoor games.',
            event_date=date.today() + timedelta(days=15),
            start_time=datetime.strptime('09:00', '%H:%M').time(),
            end_time=datetime.strptime('17:00', '%H:%M').time(),
            venue='College Sports Complex',
            event_type='sports',
            target_audience='all',
            created_by=principal_staff.id,
            is_active=True
        )
        db.session.add(event1)
        
        event2 = Event(
            title='Tech Fest 2024',
            description='Annual technology festival featuring project exhibitions, coding competitions, and tech talks.',
            event_date=date.today() + timedelta(days=45),
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            end_time=datetime.strptime('18:00', '%H:%M').time(),
            venue='Main Auditorium',
            event_type='academic',
            target_audience='all',
            created_by=staff1_profile.id,
            is_active=True
        )
        db.session.add(event2)
        
        db.session.commit()
        
        # Create library resources
        print("Creating library resources...")
        resource1 = LibraryResource(
            title='Database System Concepts',
            subject='Database Systems',
            course='Computer Science',
            year=2,
            semester=3,
            resource_type='book',
            author='Silberschatz, Korth, Sudarshan',
            description='Comprehensive textbook covering fundamental database concepts.',
            added_by=staff1_profile.id,
            is_available=True
        )
        db.session.add(resource1)
        
        resource2 = LibraryResource(
            title='Database Systems Mid-Term 2022',
            subject='Database Systems',
            course='Computer Science',
            year=2,
            semester=3,
            resource_type='exam_paper',
            description='Previous year mid-term examination paper with solutions.',
            added_by=staff1_profile.id,
            is_available=True
        )
        db.session.add(resource2)
        
        resource3 = LibraryResource(
            title='Web Development Complete Guide',
            subject='Web Development',
            course='Computer Science',
            year=2,
            semester=3,
            resource_type='notes',
            author='Prof. Jane Doe',
            description='Complete lecture notes for web development course.',
            added_by=staff1_profile.id,
            is_available=True
        )
        db.session.add(resource3)
        
        db.session.commit()
        
        # Create exam results
        print("Creating exam results...")
        result1 = ExamResult(
            examination_id=exam1.id,
            student_id=student1_profile.id,
            marks_obtained=85,
            grade='A',
            remarks='Excellent performance'
        )
        db.session.add(result1)
        
        result2 = ExamResult(
            examination_id=exam1.id,
            student_id=student2_profile.id,
            marks_obtained=78,
            grade='B+',
            remarks='Good work'
        )
        db.session.add(result2)
        
        db.session.commit()
        
        # Create fee payment
        print("Creating fee payment...")
        payment1 = FeePayment(
            student_id=student1_profile.id,
            fee_structure_id=fee_structure.id,
            amount_paid=6100.0,
            payment_method='online',
            transaction_id='TXN123456789',
            status='pending',
            remarks='Semester 3 fee payment'
        )
        db.session.add(payment1)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print("\nLogin credentials:")
        print("Principal: username='principal', password='principal123'")
        print("Staff: username='staff1', password='staff123'")
        print("Student 1: username='student1', password='student123'")
        print("Student 2: username='student2', password='student123'")

if __name__ == '__main__':
    create_sample_data()
