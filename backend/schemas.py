from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class StudentCreate(BaseModel):
    name: str
    roll_no: str
    class_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    rfid_tag: Optional[str] = None


class StudentResponse(BaseModel):
    student_id: int
    name: str
    roll_no: str
    class_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    rfid_tag: Optional[str] = None
    face_image_path: Optional[str] = None
    embedding_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceResponse(BaseModel):
    attendance_id: int
    student_id: int
    date: date
    checkin_time: datetime
    mode_used: str
    confidence_score: Optional[float] = None
    status: str

    class Config:
        from_attributes = True