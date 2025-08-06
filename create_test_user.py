from app import create_app, db
from app.models import User, Student
from datetime import date

def create_test_user():
    app = create_app()
    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(username='teststudent').first()
        if existing_user:
            print("Test student user already exists!")
            print("Login with: username='teststudent', password='test123'")
            return
        
        # Create a simple test student user
        test_user = User(username='teststudent', email='test@student.com', role='student')
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        
        # Create student profile
        test_student = Student(
            user_id=test_user.id,
            student_id='TEST001',
            first_name='Test',
            last_name='Student',
            date_of_birth=date(2000, 1, 1),
            gender='Other',
            phone='+1234567890',
            address='Test Address',
            course='Computer Science',
            year=1,
            semester=1,
            admission_date=date.today()
        )
        db.session.add(test_student)
        db.session.commit()
        
        print("Test student user created successfully!")
        print("Login credentials:")
        print("Username: teststudent")
        print("Password: test123")
        print("Role: student")

if __name__ == '__main__':
    create_test_user()
