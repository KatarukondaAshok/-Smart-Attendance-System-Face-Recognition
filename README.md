<img width="1965" height="1060" alt="image" src="https://github.com/user-attachments/assets/9923dae9-22ee-43de-b894-0bc52caec1f5" /># 📸 Smart Attendance System — Face Recognition Based

An automated **Face Recognition Attendance System** built using **FastAPI** and **Streamlit**.
The system captures student faces through a webcam, recognizes them in real time, and automatically marks attendance based on timetable sessions.

Designed for educational institutions to reduce manual attendance effort while ensuring fast and reliable attendance tracking.

---

# 🚀 Features

* 📷 Webcam-based student registration and attendance
* 🧠 Face recognition using OpenCV + embedding comparison
* 🗓️ Timetable-aware attendance system
* 👨‍🏫 Teacher dashboard for attendance management
* 🎓 Student portal for attendance tracking
* 🛡️ Admin dashboard with alert threshold settings
* 📊 Attendance reports & defaulter detection
* 🔒 Duplicate attendance prevention
* ⚡ FastAPI backend with Streamlit frontend
* 💾 SQLite database integration

---

# 🏗️ System Architecture

```text
                ┌─────────────────────┐
                │   Streamlit UI      │
                │  (Frontend Client)  │
                └─────────┬───────────┘
                          │ HTTP Requests
                          ▼
                ┌─────────────────────┐
                │     FastAPI API     │
                │      Backend        │
                └─────────┬───────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼                                ▼
 ┌─────────────────┐              ┌─────────────────┐
 │ SQLite Database │              │ Face Recognition│
 │ attendance.db   │              │ OpenCV + NumPy  │
 └─────────────────┘              └─────────────────┘
```

---

# 📂 Project Structure

```text
attendance-system/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── face_utils.py
│   ├── attendance_utils.py
│   │
│   └── routes/
│       ├── students.py
│       ├── attendance.py
│       └── reports.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── embeddings/
│   ├── student_images/
│   ├── temp_uploads/
│   ├── test_images/
│   └── daily_report.csv
│
├── attendance.db
├── requirements.txt
└── README.md
```

---

# 🧠 Face Recognition Workflow

## 1️⃣ Student Registration

```text
Teacher opens Register Student page
        ↓
Fill student details
        ↓
Capture face using webcam
        ↓
Image sent to FastAPI backend
        ↓
OpenCV detects largest face
        ↓
Face preprocessing applied
        ↓
Embedding stored as .npy file
        ↓
Student registered successfully
```

---

## 2️⃣ Attendance Marking

```text
Student opens Mark Attendance page
        ↓
Select class
        ↓
Capture image from webcam
        ↓
Image sent to backend
        ↓
Current session detected from timetable
        ↓
Stored embeddings loaded
        ↓
MAD score calculated
        ↓
Face matched successfully
        ↓
Attendance saved into database
```

---

# 🧠 Face Recognition Algorithm

| Step          | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| Detection     | OpenCV Haar Cascade (`haarcascade_frontalface_default.xml`) |
| Preprocessing | Grayscale → Resize → Histogram Equalization → Gaussian Blur |
| Embedding     | Processed pixel array saved as `.npy`                       |
| Matching      | Mean Absolute Difference (MAD)                              |
| Threshold     | MAD score < 72 = Recognized                                 |

---

# 🗓️ Timetable Configuration

Attendance can only be marked during active sessions.

| Time          | Status               |
| ------------- | -------------------- |
| 10:00 – 11:00 | Session 1            |
| 11:00 – 12:00 | Session 2            |
| 12:00 – 12:30 | 🍽️ Lunch Break      |
| 12:30 – 13:00 | Session 3            |
| Outside Hours | ❌ Attendance Blocked |

Supported Classes:

* CSE
* CSE-AI
* ECE

---

# 🛠️ Tech Stack

| Layer             | Technology |
| ----------------- | ---------- |
| Backend           | FastAPI    |
| Frontend          | Streamlit  |
| Database          | SQLite     |
| ORM               | SQLAlchemy |
| Validation        | Pydantic   |
| Face Detection    | OpenCV     |
| Embeddings        | NumPy      |
| API Communication | Requests   |

---

# ⚙️ Installation & Setup

## 📌 Prerequisites

* Python 3.9+
* Webcam
* Git

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/attendance-system.git

cd attendance-system
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Start FastAPI Backend

```bash
uvicorn backend.app:app --reload --port 8000
```

Backend runs on:

```text
http://localhost:8000
```

---

## 4️⃣ Start Streamlit Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📡 API Endpoints

# 👨‍🎓 Students

| Method | Endpoint                     | Description          |
| ------ | ---------------------------- | -------------------- |
| POST   | `/students`                  | Register new student |
| GET    | `/students`                  | Get all students     |
| GET    | `/students/{id}`             | Get student by ID    |
| POST   | `/students/{id}/upload-face` | Upload student face  |

---

# 📷 Attendance

| Method | Endpoint                              | Description                   |
| ------ | ------------------------------------- | ----------------------------- |
| POST   | `/attendance/recognize-and-mark`      | Recognize & mark attendance   |
| GET    | `/attendance/logs`                    | Get attendance logs           |
| GET    | `/attendance/student/{id}/percentage` | Student attendance percentage |
| GET    | `/attendance/percentages`             | All attendance percentages    |
| PUT    | `/attendance/manual-mark/{id}`        | Manual attendance marking     |

---

# 📊 Reports

| Method | Endpoint                  | Description                 |
| ------ | ------------------------- | --------------------------- |
| GET    | `/reports/alert-settings` | Get alert threshold         |
| POST   | `/reports/alert-settings` | Update threshold            |
| GET    | `/reports/defaulters`     | Get low attendance students |

---

# 🖥️ Frontend Modules

| Page              | Description                     |
| ----------------- | ------------------------------- |
| Register Student  | Add student + capture face      |
| Mark Attendance   | Face recognition attendance     |
| Teacher Dashboard | View logs & manual marking      |
| Student Portal    | Attendance percentage & history |
| Admin Dashboard   | Manage thresholds & students    |

---

# 📸 Screenshots

## 🔄 System Workflow
<img width="1701" height="957" alt="image" src="https://github.com/user-attachments/assets/c4e1ffe6-3384-47cc-a52d-76f0ed2a3f91" />



---

## 👨‍🏫 Teacher Dashboard

View real-time attendance logs and manually override attendance when needed.

<img width="1701" height="957" alt="image" src="https://github.com/user-attachments/assets/f7e4e32c-99c7-40a1-ac5e-0c9c6cb9e5aa" />



---

## 🛡️ Admin Dashboard

Monitor attendance percentages, configure alert thresholds, and manage attendance analytics.

<img width="2081" height="1125" alt="image" src="https://github.com/user-attachments/assets/5fa8c6a2-ae97-4858-8dd1-55f4f1dfd26d" />


---

## 🎓 Student Portal

Students can view attendance percentage, total classes, and attendance history.

![Student Portal](images/student_portal.png)
<img width="2000" height="939" alt="image" src="https://github.com/user-attachments/assets/5b563996-41f1-47aa-aa11-d79299b31bbd" />


---

## 📷 Register Student

Capture student face using webcam and store embeddings for recognition.

<img width="2000" height="939" alt="image" src="https://github.com/user-attachments/assets/f7ebfc67-0fe3-4e06-9f26-be763f1f05cb" />


---

## ✅ Mark Attendance

Students can mark attendance through real-time face recognition.

![Mark Attendance](images/mark_attendance.png)
<img width="1921" height="1106" alt="image" src="https://github.com/user-attachments/assets/d85b12af-8171-46e7-81f7-94f148d26ce5" />


---

# 🔒 Duplicate Prevention Logic

The system prevents multiple attendance entries for the same student within the same session and day.

Validation checks include:

* Student already marked today?
* Correct class selected?
* Active session available?
* Face confidence score valid?

---

# 📊 Attendance Percentage Calculation

```text
Attendance % =
(Total Present Sessions / Total Conducted Sessions) × 100
```

Students below the configured threshold are automatically flagged as defaulters.

---

# 📁 Data Storage

| Folder/File            | Purpose                    |
| ---------------------- | -------------------------- |
| `data/embeddings/`     | Stored face embeddings     |
| `data/student_images/` | Registered face images     |
| `data/temp_uploads/`   | Temporary uploaded files   |
| `attendance.db`        | SQLite database            |
| `daily_report.csv`     | Exported attendance report |

---

# 🔮 Future Enhancements

* ✅ Deep Learning face embeddings (FaceNet / Dlib)
* ✅ Multi-face attendance support
* ✅ Email alerts for low attendance
* ✅ Cloud database integration
* ✅ Docker deployment
* ✅ Mobile application support
* ✅ Real-time CCTV attendance monitoring

---

# 🤝 Contributing

Contributions are welcome.

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature-name

# Commit changes
git commit -m "Added new feature"

# Push changes
git push origin feature-name
```

Then create a Pull Request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Ashok Katarukonda

* B.Tech Engineering Student
* Passionate about AI, Computer Vision & Full Stack Development

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 📢 Share with others

---
