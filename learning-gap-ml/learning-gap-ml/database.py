import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = 'learning_gap.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all required tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table (Teachers and Students)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        name TEXT NOT NULL,
        class_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Assignments table
    c.execute('''CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        subject TEXT NOT NULL,
        class_name TEXT NOT NULL,
        due_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users(id)
    )''')
    
    # Assignment submissions
    c.execute('''CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        submission_text TEXT,
        file_path TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'submitted',
        FOREIGN KEY (assignment_id) REFERENCES assignments(id),
        FOREIGN KEY (student_id) REFERENCES users(id)
    )''')
    
    # Progress tracking
    c.execute('''CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        topics_completed INTEGER DEFAULT 0,
        assessment_score REAL,
        last_accessed TIMESTAMP,
        materials_viewed INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES users(id)
    )''')
    
    # Search history (for analytics)
    c.execute('''CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        query TEXT NOT NULL,
        searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

def register_user(username, password, email, role, name, class_name=None):
    """Register a new user"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        c.execute('''INSERT INTO users (username, password, email, role, name, class_name) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (username, hashed_password, email, role, name, class_name))
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate user"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return True, dict(user)
    return False, None

def get_user(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def create_assignment(teacher_id, title, description, subject, class_name, due_date):
    """Create a new assignment"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO assignments (teacher_id, title, description, subject, class_name, due_date)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (teacher_id, title, description, subject, class_name, due_date))
    conn.commit()
    assignment_id = c.lastrowid
    conn.close()
    return assignment_id

def get_assignments_by_class(class_name):
    """Get all assignments for a class"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT a.*, u.name as teacher_name FROM assignments a 
                 JOIN users u ON a.teacher_id = u.id 
                 WHERE a.class_name = ? ORDER BY a.due_date DESC''', (class_name,))
    assignments = [dict(row) for row in c.fetchall()]
    conn.close()
    return assignments

def get_assignment(assignment_id):
    """Get assignment by ID"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT a.*, u.name as teacher_name FROM assignments a 
                 JOIN users u ON a.teacher_id = u.id 
                 WHERE a.id = ?''', (assignment_id,))
    assignment = c.fetchone()
    conn.close()
    return dict(assignment) if assignment else None

def submit_assignment(assignment_id, student_id, submission_text, file_path=None):
    """Submit an assignment"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO submissions (assignment_id, student_id, submission_text, file_path)
                 VALUES (?, ?, ?, ?)''',
              (assignment_id, student_id, submission_text, file_path))
    conn.commit()
    conn.close()

def get_submissions_for_assignment(assignment_id):
    """Get all submissions for an assignment"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT s.*, u.name as student_name FROM submissions s
                 JOIN users u ON s.student_id = u.id
                 WHERE s.assignment_id = ? ORDER BY s.submitted_at DESC''', (assignment_id,))
    submissions = [dict(row) for row in c.fetchall()]
    conn.close()
    return submissions

def update_progress(student_id, subject, topics_completed=None, assessment_score=None, materials_viewed=None):
    """Update student progress"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if record exists
    c.execute('SELECT id FROM progress WHERE student_id = ? AND subject = ?', (student_id, subject))
    exists = c.fetchone()
    
    if exists:
        update_parts = ['updated_at = CURRENT_TIMESTAMP']
        params = []
        
        if topics_completed is not None:
            update_parts.append('topics_completed = ?')
            params.append(topics_completed)
        if assessment_score is not None:
            update_parts.append('assessment_score = ?')
            params.append(assessment_score)
        if materials_viewed is not None:
            update_parts.append('materials_viewed = ?')
            params.append(materials_viewed)
        
        params.extend([student_id, subject])
        query = f"UPDATE progress SET {', '.join(update_parts)} WHERE student_id = ? AND subject = ?"
        c.execute(query, params)
    else:
        c.execute('''INSERT INTO progress (student_id, subject, topics_completed, assessment_score, materials_viewed)
                     VALUES (?, ?, ?, ?, ?)''',
                  (student_id, subject, topics_completed or 0, assessment_score, materials_viewed or 0))
    
    conn.commit()
    conn.close()

def get_student_progress(student_id):
    """Get all progress records for a student"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM progress WHERE student_id = ? ORDER BY subject', (student_id,))
    progress = [dict(row) for row in c.fetchall()]
    conn.close()
    return progress

def record_search(user_id, query):
    """Record user search query"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO search_history (user_id, query) VALUES (?, ?)', (user_id, query))
    conn.commit()
    conn.close()

def get_popular_searches():
    """Get popular search queries"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT query, COUNT(*) as count FROM search_history 
                 GROUP BY query ORDER BY count DESC LIMIT 10''')
    searches = [dict(row) for row in c.fetchall()]
    conn.close()
    return searches
