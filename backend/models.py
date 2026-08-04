from sqlalchemy import Column, Integer, String, DateTime, Float, Date, Boolean
from datetime import datetime, date

from backend.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, unique=True, nullable=False, index=True)
    class_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, nullable=True)
    rfid_tag = Column(String, unique=True, nullable=True)

    face_image_path = Column(String, nullable=True)
    embedding_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    subject_name = Column(String, nullable=True)
    session_start = Column(String, nullable=True)
    session_end = Column(String, nullable=True)
    date = Column(Date, default=date.today, index=True)
    checkin_time = Column(DateTime, default=datetime.utcnow)
    mode_used = Column(String, default="face")
    confidence_score = Column(Float, nullable=True)
    status = Column(String, default="present")


class AlertSetting(Base):
    __tablename__ = "alert_settings"

    id = Column(Integer, primary_key=True, index=True)
    threshold_percentage = Column(Float, default=75.0)
    email_enabled = Column(Boolean, default=False)
    sms_enabled = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)