from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
import tempfile

from backend.database import get_db
from backend.models import Student
from backend.schemas import StudentCreate, StudentResponse
from backend.face_utils import save_cropped_face_image, generate_face_embedding_from_image

router = APIRouter(prefix="/students", tags=["Students"])

UPLOAD_DIR = "data/student_images"
TEMP_DIR = "data/temp_uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.roll_no == student.roll_no).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Roll number already exists")

    if student.email:
        existing_email = db.query(Student).filter(Student.email == student.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

    new_student = Student(
        name=student.name,
        roll_no=student.roll_no,
        class_name=student.class_name,
        email=student.email,
        phone=student.phone,
        rfid_tag=student.rfid_tag,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/{student_id}/upload-face")
def upload_face(student_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    temp_extension = os.path.splitext(file.filename)[1] or ".jpg"
    temp_path = os.path.join(TEMP_DIR, f"temp_{student_id}{temp_extension}")
    final_face_path = os.path.join(UPLOAD_DIR, f"student_{student_id}.jpg")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        save_cropped_face_image(temp_path, final_face_path)
        embedding_path = generate_face_embedding_from_image(temp_path, student_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    student.face_image_path = final_face_path
    student.embedding_path = embedding_path
    db.commit()
    db.refresh(student)

    return {
        "message": "Student registered and face saved successfully",
        "student_id": student.student_id,
        "student_name": student.name,
        "roll_no": student.roll_no,
        "class_name": student.class_name,
        "face_image_path": student.face_image_path,
        "embedding_path": student.embedding_path
    }