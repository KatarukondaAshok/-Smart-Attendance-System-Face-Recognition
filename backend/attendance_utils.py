from sqlalchemy.orm import Session
from backend.models import AttendanceLog, Student, AlertSetting


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

    return {
        "student_id": student_id,
        "present_days": present_days,
        "total_days": total_days,
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


def get_or_create_alert_setting(db: Session):
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

    return setting


def get_defaulters(db: Session):
    setting = get_or_create_alert_setting(db)
    threshold = setting.threshold_percentage

    all_stats = get_all_student_percentages(db)

    return [
        row for row in all_stats
        if row["attendance_percentage"] < threshold
    ]