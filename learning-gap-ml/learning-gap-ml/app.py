from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from model import load_model, predict_risk

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CLASSES_FILE = 'classes_subjects.json'

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

# Teacher Upload
@app.route('/teacher', methods=['GET','POST'])
def teacher():
    message = None
    message_type = None
    
    if request.method == 'POST':
        class_name = request.form.get('class_name', '').strip()
        subject = request.form.get('subject', '').strip()
        date = request.form.get('date', '')
        content = request.form.get('content', '').strip()
        file = request.files.get('file')

        # Validate inputs
        if not class_name or not subject or not date:
            message = "Please fill in all required fields (Class, Subject, Date)"
            message_type = "error"
        elif not content and not file:
            message = "Please either write notes or upload a file"
            message_type = "error"
        else:
            try:
                # Create folder for class/subject/date
                folder_path = os.path.join(app.config['UPLOAD_FOLDER'], class_name, subject, date)
                os.makedirs(folder_path, exist_ok=True)

                # Save content as text file if content is written
                if content:
                    with open(os.path.join(folder_path, 'notes.txt'), 'w', encoding='utf-8') as f:
                        f.write(content)

                # Save uploaded file
                if file and file.filename:
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(folder_path, filename))
                    else:
                        message = "File type not allowed. Please use: PDF, TXT, DOC, DOCX"
                        message_type = "error"
                        return render_template('teacher.html', message=message, message_type=message_type)

                message = "✓ Content uploaded successfully!"
                message_type = "success"
            except Exception as e:
                message = f"Error uploading content: {str(e)}"
                message_type = "error"

    return render_template('teacher.html', message=message, message_type=message_type)

# Student View
@app.route('/student', methods=['GET','POST'])
def student():
    content_list = []
    classes_subjects = get_available_classes_subjects()
    if request.method == 'POST':
        class_name = request.form['class_name']
        subject = request.form['subject']
        upload_root = app.config['UPLOAD_FOLDER']

        def gather_from_folder(class_name_val, subject_val):
            results = []
            base = os.path.join(upload_root, class_name_val, subject_val)
            if not os.path.exists(base):
                return results
            for date_folder in sorted(os.listdir(base)):
                date_path = os.path.join(base, date_folder)
                try:
                    files = os.listdir(date_path)
                except Exception:
                    continue

                files_list = []
                for f in files:
                    rel_path = os.path.join(class_name_val, subject_val, date_folder, f).replace('\\', '/')
                    files_list.append({'name': f, 'path': rel_path})

                results.append({'class': class_name_val, 'subject': subject_val, 'date': date_folder, 'files': files_list})
            return results

        # Support selecting all classes or all subjects
        if class_name == 'ALL':
            # iterate all classes
            for cls in sorted(os.listdir(upload_root)):
                class_path = os.path.join(upload_root, cls)
                if not os.path.isdir(class_path):
                    continue
                if subject and subject != 'ALL':
                    content_list.extend(gather_from_folder(cls, subject))
                else:
                    # gather from all subjects under this class
                    for subj in sorted(os.listdir(class_path)):
                        subj_path = os.path.join(class_path, subj)
                        if not os.path.isdir(subj_path):
                            continue
                        content_list.extend(gather_from_folder(cls, subj))
        else:
            # specific class selected
            if subject == 'ALL':
                # iterate all subjects under the selected class
                class_path = os.path.join(upload_root, class_name)
                if os.path.exists(class_path):
                    for subj in sorted(os.listdir(class_path)):
                        subj_path = os.path.join(class_path, subj)
                        if not os.path.isdir(subj_path):
                            continue
                        content_list.extend(gather_from_folder(class_name, subj))
            else:
                content_list = gather_from_folder(class_name, subject)

    return render_template('student.html', content_list=content_list, classes_subjects=classes_subjects)

# Risk Prediction
@app.route('/risk-prediction', methods=['GET', 'POST'])
def risk_prediction():
    prediction = None
    risk_info = None
    message = None
    message_type = None
    
    if request.method == 'POST':
        try:
            # Get form data
            student_name = request.form.get('student_name', '').strip()
            class_name = request.form.get('class_name', '').strip()
            days_absent = float(request.form.get('days_absent', 0))
            missed_topics = float(request.form.get('missed_topics', 0))
            avg_marks = float(request.form.get('avg_marks', 0))
            difficulty_score = float(request.form.get('difficulty_score', 0))
            
            # Validate inputs
            if not student_name or not class_name:
                message = "Please provide student name and class"
                message_type = "error"
            elif days_absent < 0 or missed_topics < 0 or avg_marks < 0 or difficulty_score < 0:
                message = "Please enter valid non-negative values"
                message_type = "error"
            else:
                # Load model and make prediction
                model = load_model()
                data = [days_absent, missed_topics, avg_marks, difficulty_score]
                prediction = predict_risk(model, data)
                
                # Get risk level color and recommendations
                risk_level = prediction.split()[0].lower()
                if risk_level == "low":
                    risk_info = {
                        "color": "#28a745",
                        "message": "Student is performing well. Continue regular monitoring.",
                        "recommendations": [
                            "Maintain current study habits",
                            "Encourage peer mentoring",
                            "Provide advanced materials"
                        ]
                    }
                elif risk_level == "medium":
                    risk_info = {
                        "color": "#ffc107",
                        "message": "Student needs some attention. Intervention recommended.",
                        "recommendations": [
                            "Schedule one-on-one sessions",
                            "Provide additional practice materials",
                            "Encourage group study sessions",
                            "Monitor attendance closely"
                        ]
                    }
                else:  # High Risk
                    risk_info = {
                        "color": "#dc3545",
                        "message": "Student requires immediate intervention. Action needed.",
                        "recommendations": [
                            "Urgent parent/guardian communication",
                            "Assign a mentor or tutor",
                            "Create personalized study plan",
                            "Daily progress tracking",
                            "Consider counseling services"
                        ]
                    }
                message = f"Prediction generated for {student_name}"
                message_type = "success"
        except ValueError:
            message = "Please enter valid numeric values"
            message_type = "error"
        except Exception as e:
            message = f"Error: {str(e)}"
            message_type = "error"
    
    return render_template('risk_prediction.html', 
                         prediction=prediction, 
                         risk_info=risk_info,
                         message=message, 
                         message_type=message_type)


@app.route('/download/<path:filepath>')
def download_file(filepath):
    try:
        directory = os.path.dirname(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
        filename = os.path.basename(filepath)
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {str(e)}", 404

# Helper function to get available classes and subjects
def get_available_classes_subjects():
    classes = {}
    # Load from filesystem
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for class_name in os.listdir(app.config['UPLOAD_FOLDER']):
            class_path = os.path.join(app.config['UPLOAD_FOLDER'], class_name)
            if os.path.isdir(class_path):
                subjects = [s for s in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, s))]
                classes[class_name] = sorted(subjects)

    # Load from classes file and merge
    if os.path.exists(CLASSES_FILE):
        try:
            with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                if isinstance(saved, dict):
                    for cls, subs in saved.items():
                        if cls in classes:
                            # merge unique
                            combined = set(classes[cls]) | set(subs or [])
                            classes[cls] = sorted(combined)
                        else:
                            classes[cls] = sorted(list(subs or []))
        except Exception:
            pass

    return classes


def load_saved_classes():
    if os.path.exists(CLASSES_FILE):
        try:
            with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def save_classes(data):
    try:
        with open(CLASSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

if __name__ == '__main__':
    app.run(debug=True)
