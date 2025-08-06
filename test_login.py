from app import create_app, db
from app.models import User

def test_login():
    app = create_app()
    with app.app_context():
        print("Testing login credentials...")
        
        # Test the test student user
        test_user = User.query.filter_by(username='teststudent').first()
        if test_user:
            print(f"✅ Test student user found: {test_user.username}, role: {test_user.role}")
            print(f"   Password check: {test_user.check_password('test123')}")
        else:
            print("❌ Test student user not found")
        
        # Test original student users
        student1 = User.query.filter_by(username='student1').first()
        if student1:
            print(f"✅ Student1 user found: {student1.username}, role: {student1.role}")
            print(f"   Password check: {student1.check_password('student123')}")
        else:
            print("❌ Student1 user not found")
        
        # Test staff user
        staff_user = User.query.filter_by(username='staff1').first()
        if staff_user:
            print(f"✅ Staff user found: {staff_user.username}, role: {staff_user.role}")
            print(f"   Password check: {staff_user.check_password('staff123')}")
        else:
            print("❌ Staff user not found")
        
        # Test principal user
        principal_user = User.query.filter_by(username='principal').first()
        if principal_user:
            print(f"✅ Principal user found: {principal_user.username}, role: {principal_user.role}")
            print(f"   Password check: {principal_user.check_password('principal123')}")
        else:
            print("❌ Principal user not found")

if __name__ == '__main__':
    test_login()
