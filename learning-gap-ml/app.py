from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False, unique=True)
    student_class = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10))
    attendance = db.Column(db.String(10), default='Absent')
    progress = db.Column(db.Integer, default=0)
    risk_level = db.Column(db.String(20), default='Low')
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name}>'

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50))
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Material {self.title}>'

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    assignment_title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50))
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Assignment {self.assignment_title}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teacher/dashboard')
def dashboard():
    selected_class = request.args.get('class', default='8', type=str)
    students = Student.query.filter_by(student_class=int(selected_class)).all()
    total_students = len(students)
    present_today = sum(1 for student in students if student.attendance == 'Present')
    absent_today = total_students - present_today
    
    # Get assignments submitted by students in this class (most recent first)
    assignments = Assignment.query.filter_by(class_id=int(selected_class)).order_by(Assignment.submitted_date.desc()).all()
    
    return render_template('dashboard.html', total_students=total_students, present_today=present_today, absent_today=absent_today, students=students, selected_class=selected_class, assignments=assignments)

@app.route('/teacher/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.attendance = request.form['attendance']
        student.risk_level = request.form['risk_level']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('dashboard', **{'class': student.student_class}))
    return render_template('edit_student.html', student=student)

@app.route('/teacher/upload/<int:class_id>', methods=['GET', 'POST'])
def teacher_upload(class_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            title = request.form.get('title', filename)
            subject = request.form.get('subject', 'General')
            
            class_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(class_id))
            os.makedirs(class_folder, exist_ok=True)
            filepath = os.path.join(class_folder, filename)
            file.save(filepath)
            
            # Save material info to database
            material = Material(
                filename=filename,
                class_id=class_id,
                title=title,
                subject=subject,
                uploaded_date=datetime.utcnow()
            )
            db.session.add(material)
            db.session.commit()
            
            flash('Material uploaded successfully!', 'success')
            return redirect(url_for('teacher_upload', class_id=class_id))
        else:
            flash('Invalid file type', 'error')
    
    return render_template('teacher_upload.html', class_id=class_id)

@app.route('/student/dashboard')
def student_dashboard():
    selected_class = request.args.get('class', default='8', type=str)
    roll_number = request.args.get('roll', default=None, type=str)
    
    # Get current student - use roll number from query param
    current_student = None
    if roll_number:
        current_student = Student.query.filter_by(roll_number=roll_number).first()
    
    all_students = Student.query.filter_by(student_class=int(selected_class)).all()
    
    # Get uploaded materials for this class with dates
    materials = Material.query.filter_by(class_id=int(selected_class)).all()
    
    # Get student's own submissions
    student_submissions = []
    if current_student:
        student_submissions = Assignment.query.filter_by(
            student_id=current_student.id,
            class_id=int(selected_class)
        ).all()
    
    return render_template('student_dashboard.html', 
                         students=all_students, 
                         selected_class=selected_class,
                         current_student=current_student,
                         materials=materials,
                         student_submissions=student_submissions)

@app.route('/student/upload/<int:class_id>', methods=['GET', 'POST'])
def student_upload(class_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            student_name = request.form.get('student_name', 'Unknown')
            roll_number = request.form.get('roll_number', 'N/A')
            assignment_title = request.form.get('assignment', 'Assignment')
            subject = request.form.get('subject', 'General')
            
            # Find student ID
            student = Student.query.filter_by(roll_number=roll_number).first()
            student_id = student.id if student else 0
            
            student_folder = os.path.join(app.config['UPLOAD_FOLDER'], f'class_{class_id}_submissions')
            os.makedirs(student_folder, exist_ok=True)
            filepath = os.path.join(student_folder, filename)
            file.save(filepath)
            
            # Save assignment submission to database
            assignment = Assignment(
                student_id=student_id,
                student_name=student_name,
                roll_number=roll_number,
                class_id=class_id,
                filename=filename,
                assignment_title=assignment_title,
                subject=subject,
                submitted_date=datetime.utcnow()
            )
            db.session.add(assignment)
            db.session.commit()

            # Log to console for debugging
            app.logger.info(f'Assignment saved: class={class_id} roll={roll_number} file={filename} time={assignment.submitted_date}')

            flash('Assignment submitted successfully!', 'success')
            # Redirect student to their dashboard so they can immediately see the dated submission
            return redirect(url_for('student_dashboard', **{'class': class_id, 'roll': roll_number}))
        else:
            flash('Invalid file type', 'error')
    
    return render_template('student_upload.html', class_id=class_id)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:filepath>')
def download_file(filepath):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found', 'error')
            return redirect(url_for('student_dashboard'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('student_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)