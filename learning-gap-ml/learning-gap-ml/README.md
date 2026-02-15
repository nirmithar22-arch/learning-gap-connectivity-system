# Learning Gap Connectivity System

A comprehensive Flask-based web application for managing educational resources, bridging learning gaps, and facilitating communication between teachers and students.

## 🌟 Features

### 1. **User Authentication** 🔐
- Secure registration for Teachers and Students
- Login/Logout functionality
- Role-based access control
- Session management
- Password hashing for security

### 2. **Teacher Portal** 👨‍🏫
- **Upload Materials**: Share lesson notes, PDFs, and resources
- **Create Assignments**: Set homework with due dates and descriptions
- **View Submissions**: Track student assignment submissions
- **Analytics Dashboard**: Monitor class engagement and submission rates
- **Content Organization**: Auto-organize materials by Class/Subject/Date

### 3. **Student Portal** 👨‍🎓
- **Dashboard**: Personalized view of progress and assignments
- **Access Materials**: Browse and download teacher-shared resources
- **Submit Assignments**: Submit homework with text or file attachments
- **Progress Tracking**: Monitor learning progress by subject
- **At-Risk Alerts**: Identify subjects needing improvement
- **Search Materials**: Full-text search across all resources

### 4. **Assignment Management** ✅
- Create and manage assignments by class/subject
- Set due dates and descriptions
- Track student submissions
- Submit assignments with text or file attachments
- View submission details and feedback

### 5. **Progress Tracking & Analytics** 📊
- Track student progress by subject
- Record assessment scores and materials viewed
- Generate class-wide analytics
- Monitor assignment completion rates
- Visualize student engagement metrics

### 6. **Resource Search** 🔍
- Full-text search across all materials
- Popular search tracking
- Quick access to frequently searched topics
- File type filtering
- Search history analytics

## System Requirements

- Python 3.7 or higher
- Flask 2.3.2+
- Werkzeug 2.3.6+
- SQLite3 (included with Python)

## Installation & Setup

### 1. **Navigate to the project directory:**
```bash
cd learning-gap-ml
```

### 2. **Create a virtual environment (recommended):**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### 1. **Start the Flask server:**
```bash
python app.py
```

### 2. **Open your browser:**
```
http://localhost:5000
```

### 3. **Create an account:**
- Click "Register" on the homepage
- Choose your role (Teacher or Student)
- Fill in your details
- Login with your credentials

## Project Structure

```
learning-gap-ml/
├── app.py                      # Main Flask application with all routes
├── database.py                 # SQLite database management & functions
├── model.py                    # ML model for risk prediction
├── train_model.py              # Model training script
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── learning_gap.db             # SQLite database (auto-created)
├── templates/
│   ├── index.html              # Home page with feature showcase
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── teacher_dashboard.html  # Teacher main dashboard
│   ├── student_dashboard.html  # Student main dashboard
│   ├── teacher_upload.html     # Upload materials form
│   ├── student_materials.html  # Browse materials
│   ├── create_assignment.html  # Create assignment form
│   ├── submit_assignment.html  # Submit assignment form
│   ├── view_submissions.html   # View student submissions
│   ├── analytics.html          # Class analytics
│   ├── search.html             # Search materials
│   ├── risk_prediction.html    # Risk prediction tool
│   └── student.html            # Legacy student view
├── static/
│   └── style.css               # Styling
├── uploads/                    # Uploaded materials storage
│   └── <class>/<subject>/<date>/ 
├── submissions/                # Assignment submissions
│   └── <assignment_id>/
└── __pycache__/
```

## Database Schema

The application uses SQLite with the following tables:

### Users
- Stores teacher and student accounts
- Password hashing with Werkzeug security
- Role-based access (teacher/student)

### Assignments
- Assignment details and due dates
- Linked to teacher creator
- Class and subject categorization

### Submissions
- Student assignment submissions
- Text and file attachments
- Submission timestamps

### Progress
- Student subject-wise progress
- Assessment scores
- Topics completed and materials viewed

### Search History
- User search queries
- For analytics and trending topics

## User Roles

### Teacher
- Create and manage assignments
- Upload and organize learning materials
- View student submissions
- Access class analytics
- Track student progress

### Student
- Access learning materials by subject
- View and submit assignments
- Track personal progress
- Search for resources
- View at-risk subject alerts

## File Formats Supported

- 📄 **Documents**: PDF, TXT, DOC, DOCX
- 🖼️ **Images**: PNG, JPG, JPEG
- **Max file size**: 16MB

## How to Use

### For Teachers

**1. Create Account:**
   - Click Register → Choose "Teacher" role
   - Fill in name, email, username, password
   - Login

**2. Upload Materials:**
   - Go to Dashboard → "Upload Materials"
   - Select class, subject, date
   - Write notes or upload a file
   - Click "Upload Materials"

**3. Create Assignments:**
   - Go to Dashboard → "Create Assignment"
   - Enter title, description, subject, class, due date
   - Click "Create Assignment"

**4. View Submissions:**
   - Go to Dashboard → Recent Assignments section
   - Click "View Submissions" on any assignment
   - See all student submissions with details

**5. View Analytics:**
   - Go to Dashboard → "View Analytics"
   - See assignment completion rates
   - Monitor class engagement metrics

### For Students

**1. Create Account:**
   - Click Register → Choose "Student" role
   - Select your class
   - Fill in name, email, username, password
   - Login

**2. Browse Materials:**
   - Go to Dashboard → Learning Materials section
   - Select a subject
   - Click "Browse Materials"
   - Download materials by date

**3. Check Assignments:**
   - Dashboard shows "Your Assignments"
   - Click "Submit" on any assignment
   - Add text answer or upload a file
   - Click "Submit Assignment"

**4. Track Progress:**
   - Dashboard shows "Your Progress" by subject
   - See scores and materials viewed
   - Check "Areas for Improvement" section

**5. Search Materials:**
   - Use search bar at top of dashboard
   - Search by keyword, subject, or topic
   - Download results directly

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Dashboard
- `GET /dashboard` - Main dashboard (role-specific)

### Materials
- `POST /teacher/upload` - Upload materials (teacher)
- `GET /student` - Browse student materials
- `GET /download/<path>` - Download file

### Assignments
- `POST /assignments/create` - Create assignment (teacher)
- `GET /assignments/<id>/submissions` - View submissions (teacher)
- `GET /assignments/submit/<id>` - Submit assignment (student)
- `POST /assignments/submit/<id>` - Process submission

### Search & Analytics
- `GET /search` - Search materials
- `GET /analytics` - View class analytics (teacher)
- `POST /api/update-progress` - Update student progress
- `GET /api/progress/<student_id>` - Get student progress

### Risk Prediction
- `GET /risk-prediction` - Risk assessment tool
- `POST /risk-prediction` - Generate prediction

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control decorators
- Secure file uploads with validation
- CSRF protection ready
- SQL injection prevention with parameterized queries

## Configuration

### Change Development Port
Edit `app.py` - last line:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port to 5001
```

### Disable Debug Mode (Production)
```python
if __name__ == '__main__':
    app.run(debug=False)
```

### Change Secret Key (Production)
Edit `app.py` - line 12:
```python
app.secret_key = 'your-production-secret-key-here'
```

## Troubleshooting

**Port Already in Use**
```bash
# Find process on port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F
```

**Database Issues**
```bash
# Reset database
rm learning_gap.db  # or del learning_gap.db on Windows
python app.py  # Recreates database
```

**File Upload Not Working**
- Check file format (PDF, TXT, DOC, DOCX, PNG, JPG, JPEG)
- Ensure file size < 16MB
- Check uploads/ folder permissions

**Login Issues**
- Verify username and password are correct
- Check that user account was created during registration
- Clear browser cookies and try again

## Performance Tips

1. **Database Optimization**: Keep database file on local SSD
2. **File Storage**: Organize uploads folder regularly
3. **Search**: Index frequently searched terms
4. **Caching**: Enable browser caching for static files
5. **Cleanup**: Archive old submissions monthly

## Future Enhancements

- [ ] Email notifications for assignments
- [ ] Real-time collaborative document editing
- [ ] Video streaming for lessons
- [ ] Mobile app (React Native)
- [ ] Advanced AI-based recommendations
- [ ] Parent communication portal
- [ ] Attendance integration
- [ ] Grade book integration
- [ ] Automated grading for quizzes
- [ ] Live classroom sessions

## License

This project is open source for educational use.

## Support & Documentation

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Python Documentation**: https://docs.python.org/3/
- **SQLite**: https://www.sqlite.org/

## Contributors

Developed as a comprehensive educational platform for bridging learning gaps and improving student outcomes.

---

**Last Updated**: February 2026  
**Version**: 2.0 (Full Feature Release)

