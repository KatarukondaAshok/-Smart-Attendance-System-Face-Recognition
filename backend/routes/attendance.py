from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import date, datetime
import os
import shutil

from backend.database import get_db
from backend.models import Student, AttendanceLog
from backend.face_utils import load_known_embeddings, recognize_face

router = APIRouter(prefix="/attendance", tags=["Attendance"])

TEST_DIR = "data/test_images"
os.makedirs(TEST_DIR, exist_ok=True)

TIMETABLE = {
    "CSE-AI": {
        "Monday": [
            {"start": "10:00", "end": "11:00", "subject": "Artificial Intelligence"},
            {"start": "11:00", "end": "12:00", "subject": "Machine Learning"},
            {"start": "12:30", "end": "13:00", "subject": "Data Structures"},
        ],
        "Tuesday": [
            {"start": "10:00", "end": "11:00", "subject": "Operating Systems"},
            {"start": "11:00", "end": "12:00", "subject": "Database Management Systems"},
            {"start": "12:30", "end": "13:00", "subject": "Computer Networks"},
        ],
        "Wednesday": [
            {"start": "10:00", "end": "11:00", "subject": "Artificial Intelligence"},
            {"start": "11:00", "end": "12:00", "subject": "Data Structures"},
            {"start": "12:30", "end": "13:00", "subject": "Machine Learning"},
        ],
        "Thursday": [
            {"start": "10:00", "end": "11:00", "subject": "Database Management Systems"},
            {"start": "11:00", "end": "12:00", "subject": "Operating Systems"},
            {"start": "12:30", "end": "13:00", "subject": "Computer Networks"},
        ],
        "Friday": [
            {"start": "10:00", "end": "11:00", "subject": "Machine Learning"},
            {"start": "11:00", "end": "12:00", "subject": "Artificial Intelligence"},
            {"start": "12:30", "end": "13:00", "subject": "Data Structures"},
        ],
    },
    "CSE": {
        "Monday": [
            {"start": "10:00", "end": "11:00", "subject": "Programming in Python"},
            {"start": "11:00", "end": "12:00", "subject": "Data Structures"},
            {"start": "12:30", "end": "13:00", "subject": "Operating Systems"},
        ],
        "Tuesday": [
            {"start": "10:00", "end": "11:00", "subject": "Database Management Systems"},
            {"start": "11:00", "end": "12:00", "subject": "Computer Networks"},
            {"start": "12:30", "end": "13:00", "subject": "Programming in Python"},
        ],
        "Wednesday": [
            {"start": "10:00", "end": "11:00", "subject": "Data Structures"},
            {"start": "11:00", "end": "12:00", "subject": "Operating Systems"},
            {"start": "12:30", "end": "13:00", "subject": "Database Management Systems"},
        ],
        "Thursday": [
            {"start": "10:00", "end": "11:00", "subject": "Computer Networks"},
            {"start": "11:00", "end": "12:00", "subject": "Programming in Python"},
            {"start": "12:30", "end": "13:00", "subject": "Data Structures"},
        ],
        "Friday": [
            {"start": "10:00", "end": "11:00", "subject": "Operating Systems"},
            {"start": "11:00", "end": "12:00", "subject": "Database Management Systems"},
            {"start": "12:30", "end": "13:00", "subject": "Computer Networks"},
        ],
    },
    "ECE": {
        "Monday": [
            {"start": "10:00", "end": "11:00", "subject": "Digital Electronics"},
            {"start": "11:00", "end": "12:00", "subject": "Signals and Systems"},
            {"start": "12:30", "end": "13:00", "subject": "Microprocessors"},
        ],
        "Tuesday": [
            {"start": "10:00", "end": "11:00", "subject": "Communication Systems"},
            {"start": "11:00", "end": "12:00", "subject": "VLSI Design"},
            {"start": "12:30", "end": "13:00", "subject": "Digital Electronics"},
        ],
        "Wednesday": [
            {"start": "10:00", "end": "11:00", "subject": "Signals and Systems"},
            {"start": "11:00", "end": "12:00", "subject": "Microprocessors"},
            {"start": "12:30", "end": "13:00", "subject": "Communication Systems"},
        ],
        "Thursday": [
            {"start": "10:00", "end": "11:00", "subject": "VLSI Design"},
            {"start": "11:00", "end": "12:00", "subject": "Digital Electronics"},
            {"start": "12:30", "end": "13:00", "subject": "Signals and Systems"},
        ],
        "Friday": [
            {"start": "10:00", "end": "11:00", "subject": "Microprocessors"},
            {"start": "11:00", "end": "12:00", "subject": "Communication Systems"},
            {"start": "12:30", "end": "13:00", "subject": "VLSI Design"},
        ],
    }
}


def get_current_session(class_name: str):
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    class_schedule = TIMETABLE.get(class_name, {})
    day_schedule = class_schedule.get(current_day, [])

    if "12:00" <= current_time < "12:30":
        return {"is_lunch": True}

    for slot in day_schedule:
        if slot["start"] <= current_time < slot["end"]:
            return slot

    return None


def get_total_sessions_for_class(db: Session, class_name: str):
    logs = db.query(AttendanceLog).all()
    sessions = set()

    for log in logs:
        student = db.query(Student).filter(Student.student_id == log.student_id).first()
        if student and student.class_name == class_name:
            sessions.add((str(log.date), log.subject_name, log.session_start, log.session_end))

    return len(sessions)


def get_student_attendance_percentage(db: Session, student_id: int):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {
            "student_id": student_id,
            "present_days": 0,
            "total_days": 0,
            "attendance_percentage": 0.0
        }

    total_sessions = get_total_sessions_for_class(db, student.class_name)
    attended_sessions = db.query(AttendanceLog).filter(
        AttendanceLog.student_id == student_id,
        AttendanceLog.status == "present"
    ).count()

    percentage = (attended_sessions / total_sessions) * 100 if total_sessions > 0 else 0.0
    if percentage > 100:
        percentage = 100.0

    return {
        "student_id": student_id,
        "present_days": attended_sessions,
        "total_days": total_sessions,
        "attendance_percentage": round(percentage, 2)
    }


def get_all_student_percentages(db: Session):
    students = db.query(Student).all()
    result = []

    for student in students:
        stats = get_student_attendance_percentage(db, student.student_id)
        result.append({
            "student_id": student.student_id,
            "name": student.name,
            "roll_no": student.roll_no,
            "class_name": student.class_name,
            "present_days": stats["present_days"],
            "total_days": stats["total_days"],
            "attendance_percentage": stats["attendance_percentage"]
        })

    return result


@router.post("/recognize-and-mark")
def recognize_and_mark_attendance(
    file: UploadFile = File(...),
    class_name: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    session_info = get_current_session(class_name)

    if session_info is None:
        return {
            "message": f"No active class session right now for {class_name}",
            "recognized": False,
            "attendance_marked": False
        }

    if session_info.get("is_lunch"):
        return {
            "message": "Lunch break is active. Attendance cannot be marked now.",
            "recognized": False,
            "attendance_marked": False
        }

    subject_name = session_info["subject"]
    session_start = session_info["start"]
    session_end = session_info["end"]

    test_file_path = os.path.join(TEST_DIR, "latest_capture.jpg")

    with open(test_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    all_students = db.query(Student).all()

    if not all_students:
        raise HTTPException(status_code=404, detail="No students registered")

    all_embeddings, all_embedding_students = load_known_embeddings(all_students)

    if not all_embeddings:
        raise HTTPException(
            status_code=400,
            detail="No student embeddings found. Please register students first."
        )

    try:
        matched_student, confidence_score = recognize_face(
            test_file_path,
            all_embeddings,
            all_embedding_students
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not matched_student:
        return {
            "message": "Face not recognized",
            "recognized": False,
            "attendance_marked": False
        }

    if matched_student.class_name != class_name:
        return {
            "message": f"{matched_student.name} does not belong to selected class {class_name}",
            "recognized": True,
            "attendance_marked": False,
            "student_id": matched_student.student_id,
            "student_name": matched_student.name,
            "roll_no": matched_student.roll_no,
            "actual_class": matched_student.class_name,
            "selected_class": class_name,
            "subject_name": subject_name
        }

    existing_attendance = db.query(AttendanceLog).filter(
        AttendanceLog.student_id == matched_student.student_id,
        AttendanceLog.date == date.today(),
        AttendanceLog.subject_name == subject_name,
        AttendanceLog.session_start == session_start,
        AttendanceLog.session_end == session_end
    ).first()

    if existing_attendance:
        return {
            "message": f"Attendance already marked for {subject_name} ({session_start} - {session_end})",
            "recognized": True,
            "attendance_marked": False,
            "student_id": matched_student.student_id,
            "student_name": matched_student.name,
            "roll_no": matched_student.roll_no,
            "class_name": matched_student.class_name,
            "subject_name": subject_name,
            "session_start": session_start,
            "session_end": session_end
        }

    attendance = AttendanceLog(
        student_id=matched_student.student_id,
        subject_name=subject_name,
        session_start=session_start,
        session_end=session_end,
        mode_used="face",
        confidence_score=float(confidence_score) if confidence_score is not None else None,
        status="present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Attendance marked successfully",
        "recognized": True,
        "attendance_marked": True,
        "student_id": matched_student.student_id,
        "student_name": matched_student.name,
        "roll_no": matched_student.roll_no,
        "class_name": matched_student.class_name,
        "subject_name": subject_name,
        "session_start": session_start,
        "session_end": session_end,
        "date": str(attendance.date)
    }


@router.get("/logs")
def get_attendance_logs(db: Session = Depends(get_db)):
    logs = db.query(AttendanceLog).all()

    result = []
    for log in logs:
        student = db.query(Student).filter(Student.student_id == log.student_id).first()
        result.append({
            "attendance_id": log.attendance_id,
            "student_id": log.student_id,
            "student_name": student.name if student else None,
            "roll_no": student.roll_no if student else None,
            "class_name": student.class_name if student else None,
            "subject_name": log.subject_name,
            "session_start": log.session_start,
            "session_end": log.session_end,
            "date": str(log.date),
            "status": log.status
        })

    return result


@router.get("/student/{student_id}/percentage")
def get_student_percentage(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    stats = get_student_attendance_percentage(db, student_id)
    stats["student_name"] = student.name
    stats["roll_no"] = student.roll_no
    stats["class_name"] = student.class_name
    return stats


@router.get("/percentages")
def get_all_percentages(db: Session = Depends(get_db)):
    return get_all_student_percentages(db)


@router.put("/manual-mark/{student_id}")
def manual_mark_attendance(
    student_id: int,
    class_name: str,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    session_info = get_current_session(class_name)

    if session_info is None:
        return {
            "message": f"No active class session right now for {class_name}",
            "attendance_marked": False
        }

    if session_info.get("is_lunch"):
        return {
            "message": "Lunch break is active. Attendance cannot be marked now.",
            "attendance_marked": False
        }

    subject_name = session_info["subject"]
    session_start = session_info["start"]
    session_end = session_info["end"]

    existing_attendance = db.query(AttendanceLog).filter(
        AttendanceLog.student_id == student_id,
        AttendanceLog.date == date.today(),
        AttendanceLog.subject_name == subject_name,
        AttendanceLog.session_start == session_start,
        AttendanceLog.session_end == session_end
    ).first()

    if existing_attendance:
        return {
            "message": f"Attendance already marked for {subject_name} ({session_start} - {session_end})",
            "attendance_marked": False,
            "student_id": student_id
        }

    attendance = AttendanceLog(
        student_id=student_id,
        subject_name=subject_name,
        session_start=session_start,
        session_end=session_end,
        mode_used="manual",
        status="present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Attendance manually marked",
        "attendance_marked": True,
        "student_id": student_id,
        "student_name": student.name,
        "class_name": student.class_name,
        "subject_name": subject_name,
        "session_start": session_start,
        "session_end": session_end,
        "date": str(attendance.date)
    }