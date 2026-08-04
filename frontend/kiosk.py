import streamlit as st
import requests
import tempfile
import html
import os

# In the Docker Space, the FastAPI backend runs in the same container
# on 127.0.0.1:8000 (see start.sh). BACKEND_URL can be overridden via
# an environment variable if you ever split this into two services.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
BTECH_CLASSES = ["CSE-AI", "CSE", "ECE"]

st.set_page_config(page_title="Smart Attendance Kiosk", layout="wide")


def api_get(endpoint):
    try:
        return requests.get(f"{BACKEND_URL}{endpoint}")
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def api_post(endpoint, **kwargs):
    try:
        return requests.post(f"{BACKEND_URL}{endpoint}", **kwargs)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def api_put(endpoint, **kwargs):
    try:
        return requests.put(f"{BACKEND_URL}{endpoint}", **kwargs)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def show_student_card(student):
    st.markdown("### Student Details")
    col1, col2 = st.columns(2)
    col1.write(f"**Student ID:** {student.get('student_id', 'N/A')}")
    col1.write(f"**Name:** {student.get('name', 'N/A')}")
    col1.write(f"**Roll No:** {student.get('roll_no', 'N/A')}")
    col2.write(f"**Class:** {student.get('class_name', 'N/A')}")
    col2.write(f"**Email:** {student.get('email', 'N/A')}")
    col2.write(f"**Phone:** {student.get('phone', 'N/A')}")


def render_table(data, title=None):
    if title:
        st.subheader(title)

    if not data:
        st.info("No data available.")
        return

    columns = list(data[0].keys())

    table_html = """
    <style>
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 16px;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #333;
        padding: 10px;
        text-align: left;
        vertical-align: top;
    }
    .custom-table th {
        background-color: #1f2937;
        color: white;
    }
    .custom-table tr:nth-child(even) {
        background-color: #111827;
    }
    .custom-table tr:nth-child(odd) {
        background-color: #0b1220;
    }
    </style>
    <table class="custom-table">
        <thead>
            <tr>
    """

    for col in columns:
        table_html += f"<th>{html.escape(str(col))}</th>"

    table_html += "</tr></thead><tbody>"

    for row in data:
        table_html += "<tr>"
        for col in columns:
            value = row.get(col, "")
            table_html += f"<td>{html.escape(str(value))}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)


st.title("📸 Smart Attendance Kiosk")
st.write(
    "Single portal for student registration, attendance marking, "
    "teacher dashboard, student portal, and admin dashboard."
)

page = st.sidebar.radio(
    "Go to",
    [
        "Register Student",
        "Mark Attendance",
        "Teacher Dashboard",
        "Student Dashboard",
        "Admin Dashboard"
    ]
)

# Register Student
if page == "Register Student":
    st.header("Register New Student")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        roll_no = st.text_input("Roll Number")
        class_name = st.selectbox("Class Name", BTECH_CLASSES)

    with col2:
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        rfid_tag = st.text_input("RFID Tag (optional)")

    reg_img = st.camera_input("Capture student's face", key="reg_face_cam")

    # Persist the captured photo into session_state the instant it's taken,
    # so it survives reruns triggered by the Register Student button click
    # (the raw widget value can come back None on that rerun even though
    # a photo was captured, which was causing false "please capture" errors).
    if reg_img is not None:
        st.session_state["reg_face_bytes"] = reg_img.getvalue()

    if "reg_face_bytes" in st.session_state:
        st.image(st.session_state["reg_face_bytes"], caption="Captured Registration Image", use_container_width=True)

    if st.button("Register Student"):
        if not name or not roll_no or not class_name:
            st.error("Please fill Name, Roll Number, and Class Name.")
        elif "reg_face_bytes" not in st.session_state:
            st.error("Please capture student face image.")
        else:
            payload = {
                "name": name,
                "roll_no": roll_no,
                "class_name": class_name,
                "email": email if email else None,
                "phone": phone if phone else None,
                "rfid_tag": rfid_tag if rfid_tag else None
            }

            create_resp = api_post("/students/", json=payload)

            if create_resp is None:
                st.stop()

            if create_resp.status_code != 200:
                st.error(f"Student creation failed: {create_resp.text}")
            else:
                student = create_resp.json()
                student_id = student["student_id"]

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(st.session_state["reg_face_bytes"])
                    tmp_path = tmp_file.name

                with open(tmp_path, "rb") as file:
                    upload_resp = api_post(
                        f"/students/{student_id}/upload-face",
                        files={"file": ("registration.jpg", file, "image/jpeg")}
                    )

                if upload_resp is None:
                    st.stop()

                if upload_resp.status_code == 200:
                    st.success("✅ Student registered successfully")
                    show_student_card(student)
                    # Clear the captured photo so the next registration starts fresh
                    del st.session_state["reg_face_bytes"]
                else:
                    st.error(f"Face upload failed: {upload_resp.text}")

# Mark Attendance
elif page == "Mark Attendance":
    st.header("Mark Attendance")

    class_name = st.selectbox("Select Class", BTECH_CLASSES)
    att_img = st.camera_input("Capture your face", key="att_face_cam")

    if att_img is not None:
        st.session_state["att_face_bytes"] = att_img.getvalue()

    if "att_face_bytes" in st.session_state:
        st.image(st.session_state["att_face_bytes"], caption="Captured Image", use_container_width=True)

    if st.button("Mark Attendance"):
        if "att_face_bytes" not in st.session_state:
            st.error("Please capture your face first.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(st.session_state["att_face_bytes"])
                tmp_path = tmp_file.name

            with open(tmp_path, "rb") as file:
                response = api_post(
                    "/attendance/recognize-and-mark",
                    files={"file": ("captured.jpg", file, "image/jpeg")},
                    data={"class_name": class_name}
                )

            if response is None:
                st.stop()

            if response.status_code == 200:
                result = response.json()

                if result.get("recognized") and result.get("attendance_marked"):
                    st.success(
                        f"✅ Attendance marked for {result.get('student_name', 'Student')} "
                        f"({result.get('roll_no', 'N/A')}) - "
                        f"{result.get('class_name', class_name)} / "
                        f"{result.get('subject_name', 'Current Session')} "
                        f"[{result.get('session_start', '')} - {result.get('session_end', '')}]"
                    )
                    # Clear the captured photo so the next person's capture starts fresh
                    if "att_face_bytes" in st.session_state:
                        del st.session_state["att_face_bytes"]

                elif result.get("recognized") and not result.get("attendance_marked"):
                    if result.get("actual_class") and result.get("selected_class"):
                        st.error(
                            f"❌ {result.get('student_name', 'Student')} belongs to "
                            f"{result.get('actual_class')}, not {result.get('selected_class')}. "
                            f"Attendance not marked."
                        )
                    else:
                        st.warning(result.get("message", "Attendance already marked"))
                else:
                    st.error(result.get("message", "Face not recognized"))
            else:
                st.error(f"Backend Error: {response.text}")

# Teacher Dashboard
elif page == "Teacher Dashboard":
    st.header("Teacher Dashboard")

    class_name = st.selectbox("Select Class", BTECH_CLASSES, key="teacher_class")

    logs_resp = api_get("/attendance/logs")
    students_resp = api_get("/students/")

    if logs_resp and students_resp and logs_resp.status_code == 200 and students_resp.status_code == 200:
        logs = logs_resp.json()
        students = students_resp.json()

        filtered_logs = [
            log for log in logs
            if log.get("class_name") == class_name
        ]

        render_table(filtered_logs, f"Today's Attendance Logs - {class_name}")

        st.subheader("Manual Attendance Override")
        class_students = [s for s in students if s.get("class_name") == class_name]

        if class_students:
            student_map = {
                f"{row['student_id']} - {row['name']} ({row['roll_no']})": row["student_id"]
                for row in class_students
            }

            selected = st.selectbox("Select Student", list(student_map.keys()))

            if st.button("Mark Attendance Manually"):
                student_id = student_map[selected]
                resp = api_put(
                    f"/attendance/manual-mark/{student_id}",
                    params={"class_name": class_name}
                )

                if resp and resp.status_code == 200:
                    result = resp.json()

                    if result.get("attendance_marked"):
                        st.success(
                            f"✅ Attendance marked for {result.get('student_name')} "
                            f"- {result.get('subject_name')} "
                            f"[{result.get('session_start')} - {result.get('session_end')}]"
                        )
                    else:
                        st.warning(result.get("message", "Attendance not marked"))
                else:
                    st.error("Manual attendance failed")
        else:
            st.info("No students available.")
    else:
        st.error("Unable to load teacher dashboard.")

# Student Dashboard
elif page == "Student Dashboard":
    st.header("Student Dashboard")

    student_id = st.number_input("Enter Student ID", min_value=1, step=1)

    if st.button("View My Attendance"):
        student_resp = api_get(f"/students/{student_id}")
        percentage_resp = api_get(f"/attendance/student/{student_id}/percentage")
        logs_resp = api_get("/attendance/logs")

        if (
            student_resp
            and percentage_resp
            and logs_resp
            and student_resp.status_code == 200
            and percentage_resp.status_code == 200
            and logs_resp.status_code == 200
        ):
            student = student_resp.json()
            percentage = percentage_resp.json()
            logs = logs_resp.json()

            show_student_card(student)

            st.subheader("Attendance Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Attendance %", f"{percentage['attendance_percentage']}%")
            col2.metric("Present Classes", percentage["present_days"])
            col3.metric("Total Classes", percentage["total_days"])

            student_logs = [log for log in logs if log.get("student_id") == student_id]

            cleaned_logs = []
            for log in student_logs:
                cleaned_logs.append({
                    "attendance_id": log.get("attendance_id"),
                    "student_id": log.get("student_id"),
                    "student_name": log.get("student_name"),
                    "roll_no": log.get("roll_no"),
                    "class_name": log.get("class_name"),
                    "subject_name": log.get("subject_name"),
                    "session_start": log.get("session_start"),
                    "session_end": log.get("session_end"),
                    "date": log.get("date"),
                    "status": log.get("status")
                })

            render_table(cleaned_logs, "Attendance History")
        else:
            st.error("Student not found or backend unavailable.")

# Admin Dashboard
elif page == "Admin Dashboard":
    st.header("Admin Dashboard")

    students_resp = api_get("/students/")
    percentages_resp = api_get("/attendance/percentages")
    settings_resp = api_get("/reports/alert-settings")

    if (
        students_resp
        and percentages_resp
        and settings_resp
        and students_resp.status_code == 200
        and percentages_resp.status_code == 200
        and settings_resp.status_code == 200
    ):
        students = students_resp.json()
        percentages = percentages_resp.json()
        settings = settings_resp.json()

        col1, col2 = st.columns(2)
        col1.metric("Total Students", len(students))
        col2.metric("Threshold", f"{settings['threshold_percentage']}%")

        render_table(percentages, "Attendance Percentages")

        st.subheader("Alert Configuration")
        threshold = st.slider(
            "Attendance Threshold",
            min_value=0,
            max_value=100,
            value=int(settings["threshold_percentage"])
        )
        email_enabled = st.checkbox("Email Alerts", value=settings["email_enabled"])
        sms_enabled = st.checkbox("SMS Alerts", value=settings["sms_enabled"])

        st.info("Note: actual email/SMS delivery is not implemented yet. Settings are only stored in the database.")

        if st.button("Save Alert Settings"):
            resp = api_post(
                "/reports/alert-settings",
                params={
                    "threshold_percentage": threshold,
                    "email_enabled": email_enabled,
                    "sms_enabled": sms_enabled
                }
            )
            if resp and resp.status_code == 200:
                st.success("Alert settings saved successfully")
            else:
                st.error("Failed to save alert settings")
    else:
        st.error("Unable to load admin dashboard.")