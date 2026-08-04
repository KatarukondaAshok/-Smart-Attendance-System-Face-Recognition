from fastapi import FastAPI
from backend.database import Base, engine
from backend.routes import students, attendance, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Attendance Tracking System",
    version="1.0.0"
)

app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {"message": "Attendance backend running"}