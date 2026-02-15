# 🚀 Quick Start Guide

## Getting Started in 5 Minutes

### 1. ✅ Start the Application
```bash
cd c:\learning-gap-ml\learning-gap-ml
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### 2. 🌐 Open in Browser
Visit: **http://localhost:5000**

You'll see the beautiful home page with 6 features displayed.

---

## 👨‍🏫 For Teachers

### Create Teacher Account
1. Click **"Register"** button
2. Choose role: **"Teacher"**
3. Fill in your details
4. Click **"Register"**
5. **Login** with your credentials

### Then Try These Features

#### Upload Materials
- Go to Dashboard → **"Upload Materials"**
- Fill in: Class, Subject, Date
- Write notes OR upload a file
- Click **"Upload Materials"**

#### Create Assignment
- Go to Dashboard → **"Create Assignment"**
- Fill in: Title, Subject, Class, Due Date
- Add optional description
- Click **"Create Assignment"**

#### View Student Work
- Go to Dashboard → **"Recent Assignments"**
- Click **"View Submissions"**
- See all student answers
- Download files

#### Check Analytics
- Go to Dashboard → **"View Analytics"**
- See completion rates
- Monitor student engagement

---

## 👨‍🎓 For Students

### Create Student Account
1. Click **"Register"** button
2. Choose role: **"Student"**
3. **Select your class** from dropdown
4. Fill in other details
5. Click **"Register"**
6. **Login** with your credentials

### Then Try These Features

#### Browse Learning Materials
- Dashboard → **"Learning Materials"**
- Select a subject
- Click **"Browse Materials"**
- Download any file

#### Submit Assignment
- Dashboard → **"Your Assignments"**
- Click **"Submit"** button
- Write answer OR upload file
- Click **"Submit Assignment"**

#### Check Progress
- Dashboard shows **"Your Progress"** section
- See scores by subject
- Get alerts if you need improvement

#### Search Materials
- Use **search bar** at top
- Type subject or keyword
- Find and download materials

---

## 🎯 Sample Test Data

### Teacher Login
```
Username: teacher1
Password: teacher123
(Or create your own account)
```

### Student Login
```
Username: student1
Password: student123
(Or create your own account)
```

---

## 📊 Key Features at a Glance

| Feature | Teacher | Student |
|---------|---------|---------|
| Upload Materials | ✅ | ❌ |
| Create Assignments | ✅ | ❌ |
| View Submissions | ✅ | ❌ |
| View Analytics | ✅ | ❌ |
| Browse Materials | ❌ | ✅ |
| Submit Assignments | ❌ | ✅ |
| Track Progress | ❌ | ✅ |
| Search Materials | ✅ | ✅ |

---

## ⚙️ Common Tasks

### How to Upload a Lesson
1. Login as Teacher
2. Dashboard → Upload Materials
3. Class: "8th Grade"
4. Subject: "Mathematics"
5. Date: Select today
6. Notes: Write or paste lesson
7. File: Upload PDF (optional)
8. Click Upload ✓

### How to Create Homework
1. Login as Teacher
2. Dashboard → Create Assignment
3. Title: "Chapter 5 Practice Problems"
4. Subject: "Mathematics"
5. Class: "8th Grade"
6. Due Date: Pick a date
7. Click Create ✓

### How to Access Materials (Student)
1. Login as Student
2. Dashboard → Learning Materials
3. Subject: "Mathematics"
4. Click Browse Materials
5. Download files by date ⬇️

### How to Submit Work (Student)
1. Login as Student
2. Dashboard → Your Assignments
3. Click Submit
4. Type answer or upload file
5. Click Submit Assignment ✓

---

## 🆘 Troubleshooting

### App Won't Start?
```bash
# Check you're in right folder
cd c:\learning-gap-ml\learning-gap-ml

# Check Python is installed
python --version

# Start again
python app.py
```

### Port 5000 Already Used?
```bash
# Change port in app.py (last line)
app.run(debug=True, port=5001)
# Then visit http://localhost:5001
```

### Forgot Password?
- Delete `learning_gap.db` file
- Restart app
- Create new account

### File Won't Upload?
- Check file type (PDF, TXT, DOC, DOCX, PNG, JPG)
- File size must be < 16MB
- Try different file

---

## 📱 Mobile Access

The app is mobile-friendly! You can:
- Access on phone/tablet
- Upload files from phone
- Submit assignments on go
- Check progress anytime

Try it: **http://localhost:5000** on your phone
(Make sure you're on same WiFi or use your IP)

---

## 🔑 Keyboard Shortcuts

- Press **Tab** to navigate forms
- Press **Enter** to submit
- Press **Ctrl+K** on search (if enabled)

---

## 📂 File Organization

Materials are auto-organized:
```
uploads/
└── 8th Grade/
    └── Mathematics/
        └── 2026-02-14/
            ├── notes.txt
            └── lesson.pdf
```

Submissions are stored:
```
submissions/
└── 1/  (assignment ID)
    ├── 5_math_homework.pdf  (student ID + filename)
    └── 7_answer.docx
```

---

## 🎓 Educational Tips

### For Teachers
1. **Upload regularly** - Keep materials current
2. **Create deadlines** - Use assignments for tracking
3. **Review submissions** - Give feedback on work
4. **Check analytics** - Monitor class progress
5. **Update progress** - Record assessment scores

### For Students
1. **Download materials** - Study them
2. **Submit on time** - Meet deadlines
3. **Check progress** - Know your strengths
4. **Focus on weak areas** - Improve scores
5. **Use search** - Find helpful materials

---

## 🌟 Pro Tips

✨ **Teacher Tips:**
- Create a schedule for assignments
- Organize materials by topic
- Give clear due dates
- Review submissions regularly
- Communicate with students

✨ **Student Tips:**
- Download all materials
- Submit assignments early
- Track your progress
- Focus on improvement areas
- Search for extra help

---

## 📞 Need Help?

1. **Check README.md** - Full documentation
2. **Check IMPLEMENTATION_SUMMARY.md** - Feature details
3. **Review error messages** - They're descriptive
4. **Check browser console** - For JavaScript errors

---

## 🎯 Next Steps

1. ✅ Create your account
2. ✅ Try uploading/submitting something
3. ✅ Explore all features
4. ✅ Invite others to use it
5. ✅ Send feedback

---

## 🚀 You're Ready!

**Everything is set up and working.** 

Just visit **http://localhost:5000** and start using the system!

**Questions?** Check the documentation files for detailed information.

---

**Happy Teaching & Learning! 🎓**

Last Updated: February 14, 2026  
Version: 2.0 - Full Features Release
