---
title: Smart Attendance Monitoring System Kiosk
emoji: 📸
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Smart Attendance Monitoring System Kiosk

A face-recognition based attendance system with a FastAPI backend and a
Streamlit kiosk frontend (Register Student, Mark Attendance / webcam
capture, Teacher Dashboard, Student Dashboard, Admin Dashboard), packaged
to run together in a single Docker container.

## Architecture

- `backend/` — FastAPI app (students, attendance, reports) running on
  `127.0.0.1:8000` inside the container.
- `frontend/kiosk.py` — Streamlit UI running on `0.0.0.0:7860` (the port
  Hugging Face routes external traffic to).
- `start.sh` — launches the backend first, waits for it to be ready, then
  starts the Streamlit frontend in the foreground.

## Important: storage is ephemeral by default

Free-tier Space containers use **ephemeral storage**. Anything written to
`data/` (student photos, face embeddings) or the SQLite database will be
lost whenever the container restarts (e.g. after the Space goes to sleep
from inactivity, or after a new deployment). This is expected behavior,
not a bug.

If you need registered students and attendance history to persist across
restarts, enable **Persistent Storage** for this Space under
**Settings → Persistent storage** (paid, billed per GB/month) and mount
it at `/app/data` and the sqlite file location.
