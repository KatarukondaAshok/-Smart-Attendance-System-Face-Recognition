from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
import pandas as pd

from backend.database import get_db
from backend.models import AttendanceLog, Student, AlertSetting

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_total_working_days(db: Session):
    unique_dates = db.query(AttendanceLog.date).distinct().all()
    return len(unique_dates) if unique_dates else 1


def get_student_attendance_percentage(db: Session, student_id: int):
    total_days = get_total_working_days(db)
    present_days = db.query(AttendanceLog).filter(
        AttendanceLog.student_id == student_id,
        AttendanceLog.status == "present"
    ).count()

    percentage = (present_days / total_days) * 100 if total_days > 0 else 0.0
    return round(percentage, 2)


@router.get("/daily")
def daily_report(db: Session = Depends(get_db)):
    today = date.today()
    logs = db.query(AttendanceLog).filter(AttendanceLog.date == today).all()

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
            "date": str(log.date),
            "checkin_time": str(log.checkin_time),
            "mode_used": log.mode_used,
            "status": log.status
        })

    return result


@router.get("/student-wise")
def student_wise_report(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    result = []

    for student in students:
        percentage = get_student_attendance_percentage(db, student.student_id)
        result.append({
            "student_id": student.student_id,
            "name": student.name,
            "roll_no": student.roll_no,
            "class_name": student.class_name,
            "attendance_percentage": percentage
        })

    return result


@router.get("/export/daily-csv")
def export_daily_csv(db: Session = Depends(get_db)):
    today = date.today()
    logs = db.query(AttendanceLog).filter(AttendanceLog.date == today).all()

    rows = []
    for log in logs:
        student = db.query(Student).filter(Student.student_id == log.student_id).first()
        rows.append({
            "attendance_id": log.attendance_id,
            "student_id": log.student_id,
            "student_name": student.name if student else None,
            "roll_no": student.roll_no if student else None,
            "class_name": student.class_name if student else None,
            "subject_name": log.subject_name,
            "date": str(log.date),
            "checkin_time": str(log.checkin_time),
            "mode_used": log.mode_used,
            "confidence_score": log.confidence_score,
            "status": log.status
        })

    df = pd.DataFrame(rows)
    csv_path = "data/daily_report.csv"
    df.to_csv(csv_path, index=False)

    return {
        "message": "Daily CSV report generated",
        "file_path": csv_path
    }


@router.get("/alert-settings")
def get_alert_settings(db: Session = Depends(get_db)):
    setting = db.query(AlertSetting).first()
    if not setting:
        setting = AlertSetting(
            threshold_percentage=75.0,
            email_enabled=False,
            sms_enabled=False
        )
        db.add(setting)
        db.commit()
        db.refresh(setting)

    return {
        "threshold_percentage": setting.threshold_percentage,
        "email_enabled": setting.email_enabled,
        "sms_enabled": setting.sms_enabled
    }


@router.post("/alert-settings")
def update_alert_settings(
    threshold_percentage: float = 75.0,
    email_enabled: bool = False,
    sms_enabled: bool = False,
    db: Session = Depends(get_db)
):
    setting = db.query(AlertSetting).first()

    if not setting:
        setting = AlertSetting(
            threshold_percentage=threshold_percentage,
            email_enabled=email_enabled,
            sms_enabled=sms_enabled
        )
        db.add(setting)
    else:
        setting.threshold_percentage = threshold_percentage
        setting.email_enabled = email_enabled
        setting.sms_enabled = sms_enabled

    db.commit()
    db.refresh(setting)

    return {
        "message": "Alert settings saved",
        "note": "Email/SMS delivery is not implemented yet. Only settings are stored.",
        "threshold_percentage": setting.threshold_percentage,
        "email_enabled": setting.email_enabled,
        "sms_enabled": setting.sms_enabled
    }