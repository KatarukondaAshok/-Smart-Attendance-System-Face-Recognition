📸 Smart Attendance System — Face Recognition Based
An automated student attendance tracking system powered by face recognition, built with FastAPI (backend) and Streamlit (frontend). Students are registered once with a webcam snapshot, and attendance is marked automatically by recognizing their face in real time.

🚀 Features

📷 Webcam-based face capture for student registration and attendance
🧠 Face recognition using OpenCV Haar Cascade + pixel-level embedding matching
🗓️ Timetable-aware attendance — auto-detects current subject based on day/time
👨‍🏫 Teacher Dashboard — view logs and manually override attendance
🎓 Student Portal — check personal attendance percentage and history
🛡️ Admin Dashboard — manage all students, set low-attendance alert thresholds
📊 Reports — CSV export and defaulter detection
🔒 Duplicate prevention — one entry per student per session per day


🏗️ Project Structure
attendance-system/
├── backend/
│   ├── app.py                  # FastAPI app entry point
│   ├── database.py             # SQLAlchemy DB setup (SQLite)
│   ├── models.py               # DB models: Student, AttendanceLog, AlertSetting
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── face_utils.py           # Face detection, embedding generation & recognition
│   ├── attendance_utils.py     # Attendance % calculation, defaulter logic
│   └── routes/
│       ├── students.py         # Student registration & face upload APIs
│       ├── attendance.py       # Face recognition + attendance marking APIs
│       └── reports.py          # Report generation & alert settings APIs
├── frontend/
│   └── app.py                  # Streamlit UI (all pages)
├── data/
│   ├── embeddings/             # Stored face embeddings (.npy files)
│   ├── student_images/         # Registered student face images
│   ├── temp_uploads/           # Temporary upload buffer
│   ├── test_images/            # Captured images for recognition
│   └── daily_report.csv        # Exported attendance report
├── attendance.db               # SQLite database
└── requirements.txt

🔄 How Webcam Image Capture Works
This system uses Streamlit's built-in st.camera_input() component to capture frames directly from the browser/device webcam — no third-party library required.
Step-by-Step Flow
1. 📝 Student Registration (One-time)
Teacher opens "Register Student" page
        ↓
Fills in Name, Roll No, Class, Email, Phone
        ↓
st.camera_input() opens webcam in the browser
        ↓
Student faces the camera → clicks "Capture"
        ↓
Image bytes saved to a temp .jpg file
        ↓
POST /students/ → creates DB record
        ↓
POST /students/{id}/upload-face → sends image to backend
        ↓
[face_utils.py] OpenCV detects the largest face in the image
        ↓
Face cropped → converted to grayscale → resized to 160×160
        ↓
Histogram equalization + Gaussian blur applied
        ↓
Processed face saved as student_{id}.npy (NumPy embedding)
2. 📷 Attendance Marking (Daily Use)
Student opens "Mark Attendance" page
        ↓
Selects their class (CSE / CSE-AI / ECE)
        ↓
st.camera_input() opens webcam
        ↓
Student faces the camera → clicks "Capture"
        ↓
Image bytes saved to temp file → sent to backend
        ↓
POST /attendance/recognize-and-mark
        ↓
Backend checks current time → looks up today's timetable slot
        ↓
Loads all stored .npy embeddings from data/embeddings/
        ↓
Captured face pre-processed same way as registration
        ↓
Mean Absolute Difference (MAD) computed against every embedding
        ↓
Best match selected → if MAD score < 72 → recognized ✅
        ↓
Checks: correct class? session already marked?
        ↓
AttendanceLog saved to DB with subject, session time, confidence score

🧠 Face Recognition Algorithm
StepDetailDetectionOpenCV haarcascade_frontalface_default.xmlPreprocessingGrayscale → Resize 160×160 → equalizeHist → GaussianBlur(3,3)EmbeddingRaw preprocessed pixel array saved as .npyMatchingMean Absolute Difference (MAD) between test and stored embeddingsThresholdMAD score < 72 → recognized; confidence = 100 - score

Why MAD? It's lightweight, fast, and works well for controlled indoor environments with consistent lighting.


🗓️ Timetable Configuration
The system has a hardcoded timetable for 3 classes: CSE-AI, CSE, ECE.
Attendance can only be marked during an active session.
TimeStatus10:00–11:00Session 111:00–12:00Session 212:00–12:30🍽️ Lunch Break (blocked)12:30–13:00Session 3Outside hours❌ No active session

⚙️ Installation & Setup
Prerequisites

Python 3.9+
Webcam (built-in or external)

1. Clone the Repository
bashgit clone https://github.com/your-username/attendance-system.git
cd attendance-system
2. Install Dependencies
bashpip install -r requirements.txt
3. Start the Backend (FastAPI)
bashuvicorn backend.app:app --reload --port 8000
4. Start the Frontend (Streamlit)
bashstreamlit run frontend/app.py
5. Open the App
http://localhost:8501

📡 API Endpoints
Students
MethodEndpointDescriptionPOST/students/Register a new studentGET/students/List all studentsGET/students/{id}Get student by IDPOST/students/{id}/upload-faceUpload face image & generate embedding
Attendance
MethodEndpointDescriptionPOST/attendance/recognize-and-markCapture image → recognize → mark attendanceGET/attendance/logsGet all attendance logsGET/attendance/student/{id}/percentageGet attendance % for a studentGET/attendance/percentagesGet attendance % for all studentsPUT/attendance/manual-mark/{id}Manually mark attendance for a student
Reports
MethodEndpointDescriptionGET/reports/alert-settingsGet current alert threshold settingsPOST/reports/alert-settingsUpdate alert thresholdGET/reports/defaultersList students below attendance threshold

🖥️ Frontend Pages
PageDescriptionRegister StudentFill details + capture face via webcamMark AttendanceSelect class + capture face → auto-recognizedTeacher DashboardView class logs + manually mark attendanceStudent PortalEnter Student ID → view % + historyAdmin DashboardAll students, percentages, configure alert threshold

🛠️ Tech Stack
LayerTechnologyBackendFastAPI, SQLAlchemy, PydanticFrontendStreamlitDatabaseSQLite (attendance.db)Face DetectionOpenCV (Haar Cascade)Embedding StorageNumPy .npy filesHTTP CommunicationPython requests
