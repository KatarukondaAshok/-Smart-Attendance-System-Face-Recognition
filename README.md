🎥 Smart Attendance Kiosk
🚀 AI-powered Face Recognition Attendance System built with Python, OpenCV, FastAPI, and Streamlit for real-time, contactless attendance management in classrooms.

🔗 Live Demo: huggingface.co/spaces/katarukondaashok143/smart-attendance-kiosk


📌 Features
🎥 Real-time face detection and recognition via webcam/kiosk camera
📝 One-click, automatic attendance marking — no manual roll call
👤 Student registration with face dataset capture
🗄️ SQL database integration for persistent attendance records
👩‍🏫 Teacher dashboard with live attendance logs and manual override
🎓 Student portal to view attendance history and percentage
🛠️ Admin dashboard for analytics, thresholds, and alert configuration
⚡ Fast, accurate recognition with confidence-based thresholds
🐳 Dockerized for easy, reproducible deployment


🏗️ System Architecture
Camera / Kiosk → Face Detection (OpenCV) → Face Recognition Model → Backend API (FastAPI) → Dashboards (Streamlit)

                                                                                                Reports & Alerts System

Camera / Kiosk — captures a live video feed of the student.
Face Detection (OpenCV) — locates and isolates the face in each frame.
Face Recognition Model — matches the detected face against registered face embeddings.
Backend API (FastAPI) — handles registration, verification, and attendance logging logic.
Dashboards (Streamlit) — surfaces reports and alerts to students, teachers, and admins.


🔄 Workflow


Register Student (details + face captured)

            ↓

      Stored in Database

            ↓

   Mark Attendance (Face Detection → Face Recognition)

            ↓

   ┌────────────────┬─────────────────────┬────────────────────┐

   Student Portal     Teacher Dashboard      Admin Dashboard

   • View attendance % • View attendance logs • View analytics & reports

   • Attendance history • Manual override      • Set alerts & thresholds


🖥️ Modules
1. Register Student
Captures student details (name, roll number, class, phone, optional RFID tag) along with a face sample, and stores both in the database.


2. Mark Attendance
Streams the live camera feed, runs face detection → recognition, and confirms identity (e.g. "Ashok Verified") before marking attendance as present for the selected class/session.


3. Teacher Dashboard
Shows today's attendance logs per class (roll no, name, subject, session time, date, status) with a Manual Attendance Override option for edge cases.


4. Student Portal
Lets a student look up their attendance summary and history — date, class, subject, session, and status — by student ID.


5. Admin Dashboard
Displays attendance percentages per student and lets admins configure an attendance threshold, plus toggle Email Alerts and SMS Alerts for low attendance.




🛠️ Tech Stack
Frontend / Dashboards: Streamlit
Backend API: FastAPI
Face Detection & Recognition: OpenCV
Database: SQL (SQLite/MySQL)
Libraries: OpenCV, NumPy, Pandas, SQLite/MySQL
Deployment: Docker, Hugging Face Spaces
Tools: Jupyter Notebook, Git


🧠 How It Works
Register a student's face and store the facial data + profile in the database.
Capture live video through the webcam/kiosk camera.
Detect and recognize faces in real time using OpenCV.
Verify identity against stored face embeddings with a confidence threshold.
Automatically mark attendance via the FastAPI backend and log it in the SQL database.
View results instantly through the Student, Teacher, or Admin dashboards.


📈 Highlights
👨‍💻 Developed using Object-Oriented Programming (OOP) principles.
🎯 Implemented statistical confidence thresholds to improve face recognition accuracy.
🗃️ Designed modular components for face detection, attendance management, and database operations.
🌐 Built a FastAPI backend to decouple recognition logic from the Streamlit UI.
📊 Built role-based dashboards (Student / Teacher / Admin) with configurable alerts.
🐳 Containerized the app with Docker for consistent, portable deployment.
🔄 Used Git for version control and Jupyter Notebook for testing and debugging.
