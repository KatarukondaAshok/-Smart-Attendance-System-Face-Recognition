# 🎥 Smart Attendance Kiosk

> **AI-powered Face Recognition Attendance System** built with **Python, OpenCV, FastAPI, Streamlit, and SQL** for real-time, contactless attendance management in classrooms.

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)]()
[![OpenCV](https://img.shields.io/badge/OpenCV-Face_Recognition-orange.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)]()

</p>

---

## 🚀 Live Demo

🔗 **Hugging Face Spaces**

https://huggingface.co/spaces/katarukondaashok143/smart-attendance-kiosk

---

# 📌 Features

- 🎥 Real-time face detection and recognition using webcam/kiosk camera
- 📝 Automatic attendance marking without manual roll call
- 👤 Student registration with face dataset capture
- 🗄️ SQL database integration for attendance records
- 👩‍🏫 Teacher dashboard with attendance logs and manual override
- 🎓 Student portal to view attendance history and percentage
- 🛠️ Admin dashboard with analytics, attendance thresholds, and alert configuration
- ⚡ Confidence-based face recognition for improved accuracy
- 🐳 Dockerized for reproducible deployment

---

# 🏗️ System Architecture

```text
                    Camera / Kiosk
                          │
                          ▼
              Face Detection (OpenCV)
                          │
                          ▼
             Face Recognition Model
                          │
                          ▼
                 Backend API (FastAPI)
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Student Portal    Teacher Dashboard   Admin Dashboard
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                 Reports & Alert System
```

---

# 🔄 Workflow

```text
Register Student
(details + face captured)
          │
          ▼
Store Face Data in Database
          │
          ▼
Capture Live Camera Feed
          │
          ▼
Face Detection (OpenCV)
          │
          ▼
Face Recognition
          │
          ▼
Identity Verification
          │
          ▼
Attendance Marked Automatically
          │
          ▼
 ┌──────────────┬─────────────────┬────────────────┐
 │ Student      │ Teacher         │ Admin          │
 │ Portal       │ Dashboard       │ Dashboard      │
 ├──────────────┼─────────────────┼────────────────┤
 │ Attendance % │ Live Logs       │ Analytics      │
 │ History      │ Manual Override │ Reports        │
 │ Summary      │                 │ Alerts         │
 └──────────────┴─────────────────┴────────────────┘
```

---

# 🖥️ Project Modules

## 👤 1. Register Student

- Register student details
- Capture facial dataset
- Store profile and face embeddings in the database

**Captured Information**

- Name
- Roll Number
- Class
- Phone Number
- Optional RFID Tag
- Face Dataset

---

## ✅ 2. Mark Attendance

- Live webcam streaming
- Face detection
- Face recognition
- Identity verification
- Automatic attendance marking

Example:

```
Ashok Verified ✅
Attendance Marked Successfully
```

---

## 👩‍🏫 3. Teacher Dashboard

Features:

- Today's attendance logs
- Subject-wise attendance
- Session details
- Manual attendance override

Displayed Information:

- Roll Number
- Student Name
- Subject
- Date
- Time
- Attendance Status

---

## 🎓 4. Student Portal

Students can view:

- Attendance Percentage
- Attendance History
- Subject-wise Records
- Session Details
- Attendance Status

---

## 🛠️ 5. Admin Dashboard

Administrator Features:

- Attendance Analytics
- Student-wise Attendance Percentage
- Attendance Threshold Configuration
- Email Alert Settings
- SMS Alert Settings
- Reports Dashboard

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Face Detection | OpenCV |
| Database | SQLite / MySQL |
| Programming Language | Python |
| Libraries | NumPy, Pandas, OpenCV |
| Deployment | Docker, Hugging Face Spaces |
| Version Control | Git |
| Development | Jupyter Notebook |

---

# 🧠 How It Works

### Step 1

Register a student's profile and capture facial data.

↓

### Step 2

Store face embeddings and profile information in the SQL database.

↓

### Step 3

Capture live video using the webcam or kiosk camera.

↓

### Step 4

Detect faces using OpenCV.

↓

### Step 5

Recognize the detected face by comparing it with registered embeddings.

↓

### Step 6

Verify identity using a confidence threshold.

↓

### Step 7

Automatically mark attendance through the FastAPI backend.

↓

### Step 8

Display attendance instantly in the Student, Teacher, and Admin dashboards.

---

# 📈 Project Highlights

- 👨‍💻 Designed using Object-Oriented Programming (OOP)
- 🎯 Confidence-based face recognition for improved accuracy
- 🗃️ Modular architecture for scalability and maintainability
- ⚡ FastAPI backend separated from the Streamlit frontend
- 📊 Role-based dashboards (Student, Teacher, Admin)
- 🐳 Dockerized for consistent deployment
- 🌐 Deployed on Hugging Face Spaces
- 🔄 Git version control for collaborative development
- 📒 Jupyter Notebook used for experimentation and testing

---

# 📂 Project Structure

```text
Smart-Attendance-Kiosk/
│
├── app/
│   ├── backend/
│   ├── frontend/
│   ├── models/
│   ├── database/
│   ├── services/
│   └── utils/
│
├── data/
│
├── attendance/
│
├── notebooks/
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Future Enhancements

- 📧 Email notifications for low attendance
- 📱 SMS alerts for parents and students
- 📷 Multiple camera support
- 🌍 Cloud database integration
- 🔐 Face anti-spoofing
- 📊 Advanced analytics dashboard
- ☁️ AWS/Azure deployment
- 📲 Mobile application

---

# 📝 Note

> **Current Status:** Email and SMS notifications are **not yet implemented**. The application currently stores alert preferences in the database, providing a configuration layer for future integration.

---

# 👨‍💻 Author

**Katarukonda Ashok**

- AI & Machine Learning Engineer
- Python Developer
- Computer Vision Enthusiast

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
