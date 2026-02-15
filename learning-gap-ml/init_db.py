import os
import shutil

# Backup and remove database if it exists
db_path = "instance/students.db"
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("[OK] Old database deleted")
    except Exception as e:
        print(f"[INFO] Database still in use, will recreate: {e}")

from app import app, db, Student

with app.app_context():
    # Drop all tables and recreate
    db.drop_all()
    db.create_all()
    print("[OK] Fresh database created")
    
    # 10 students for Class 8
    class8_students = [
        Student(name="Arjun Kumar", roll_number="801", student_class=8, section="A", attendance="Present", progress=85, risk_level="Low"),
        Student(name="Priya Singh", roll_number="802", student_class=8, section="B", attendance="Absent", progress=45, risk_level="High"),
        Student(name="Ravi Patel", roll_number="803", student_class=8, section="A", attendance="Present", progress=65, risk_level="Medium"),
        Student(name="Neha Desai", roll_number="804", student_class=8, section="B", attendance="Present", progress=78, risk_level="Low"),
        Student(name="Aditya Sharma", roll_number="805", student_class=8, section="A", attendance="Absent", progress=55, risk_level="High"),
        Student(name="Sneha Joshi", roll_number="806", student_class=8, section="B", attendance="Present", progress=88, risk_level="Low"),
        Student(name="Vikram Singh", roll_number="807", student_class=8, section="A", attendance="Present", progress=92, risk_level="Low"),
        Student(name="Ananya Verma", roll_number="808", student_class=8, section="B", attendance="Absent", progress=50, risk_level="High"),
        Student(name="Rohan Gupta", roll_number="809", student_class=8, section="A", attendance="Present", progress=72, risk_level="Medium"),
        Student(name="Pooja Rao", roll_number="810", student_class=8, section="B", attendance="Present", progress=81, risk_level="Low"),
    ]
    
    # 10 students for Class 9
    class9_students = [
        Student(name="Rahul Kapoor", roll_number="901", student_class=9, section="A", attendance="Present", progress=75, risk_level="Low"),
        Student(name="Divya Kumar", roll_number="902", student_class=9, section="B", attendance="Present", progress=55, risk_level="Medium"),
        Student(name="Saurav Patel", roll_number="903", student_class=9, section="A", attendance="Absent", progress=40, risk_level="High"),
        Student(name="Shruti Singh", roll_number="904", student_class=9, section="B", attendance="Present", progress=82, risk_level="Low"),
        Student(name="Aman Joshi", roll_number="905", student_class=9, section="A", attendance="Present", progress=68, risk_level="Medium"),
        Student(name="Ritika Sharma", roll_number="906", student_class=9, section="B", attendance="Absent", progress=48, risk_level="High"),
        Student(name="Nikhil Verma", roll_number="907", student_class=9, section="A", attendance="Present", progress=80, risk_level="Low"),
        Student(name="Priyanka Desai", roll_number="908", student_class=9, section="B", attendance="Present", progress=74, risk_level="Low"),
        Student(name="Harsh Gupta", roll_number="909", student_class=9, section="A", attendance="Absent", progress=52, risk_level="High"),
        Student(name="Kavya Rao", roll_number="910", student_class=9, section="B", attendance="Present", progress=79, risk_level="Low"),
    ]
    
    # 10 students for Class 10
    class10_students = [
        Student(name="Vikram Singh", roll_number="1001", student_class=10, section="A", attendance="Present", progress=95, risk_level="Low"),
        Student(name="Ananya Verma", roll_number="1002", student_class=10, section="B", attendance="Present", progress=88, risk_level="Low"),
        Student(name="Rohan Gupta", roll_number="1003", student_class=10, section="A", attendance="Absent", progress=50, risk_level="High"),
        Student(name="Zara Khan", roll_number="1004", student_class=10, section="B", attendance="Present", progress=85, risk_level="Low"),
        Student(name="Arjun Nair", roll_number="1005", student_class=10, section="A", attendance="Present", progress=92, risk_level="Low"),
        Student(name="Simran Kaur", roll_number="1006", student_class=10, section="B", attendance="Absent", progress=58, risk_level="High"),
        Student(name="Rajesh Kumar", roll_number="1007", student_class=10, section="A", attendance="Present", progress=87, risk_level="Low"),
        Student(name="Aditi Singh", roll_number="1008", student_class=10, section="B", attendance="Present", progress=80, risk_level="Low"),
        Student(name="Mohan Rao", roll_number="1009", student_class=10, section="A", attendance="Absent", progress=45, risk_level="High"),
        Student(name="Navya Patel", roll_number="1010", student_class=10, section="B", attendance="Present", progress=89, risk_level="Low"),
    ]
    
    all_students = class8_students + class9_students + class10_students
    for student in all_students:
        db.session.add(student)
    db.session.commit()
    
    print("[OK] 10 students added to Class 8")
    print("[OK] 10 students added to Class 9")
    print("[OK] 10 students added to Class 10")
    print("[OK] Total: 30 students in database")
