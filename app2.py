import streamlit as st
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# -----------------------------
# Configuration
# -----------------------------
STUDENT_FOLDER = "students"
ATTENDANCE_FILE = "attendance.csv"

os.makedirs(STUDENT_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="AI Face Recognition Attendance",
    page_icon="📸",
    layout="wide"
)

# -----------------------------
# Functions
# -----------------------------

def load_known_faces():
    known_encodings = []
    known_names = []

    for file in os.listdir(STUDENT_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(STUDENT_FOLDER, file)
            image = face_recognition.load_image_file(image_path)

            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])

                name = os.path.splitext(file)[0]
                known_names.append(name)

    return known_encodings, known_names


def mark_attendance(name):
    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_csv(ATTENDANCE_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])

    # Check whether attendance is already marked today
    already_marked = (
        (df["Name"] == name) &
        (df["Date"] == date)
    ).any()

    if not already_marked:
        new_record = pd.DataFrame({
            "Name": [name],
            "Date": [date],
            "Time": [time],
            "Status": ["Present"]
        })

        df = pd.concat(
            [df, new_record],
            ignore_index=True
        )

        df.to_csv(ATTENDANCE_FILE, index=False)

        return True

    return False


# -----------------------------
# Title
# -----------------------------

st.title("📸 AI Face Recognition Attendance System")

st.write(
    "Register students and automatically mark attendance "
    "using face recognition."
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Menu")

option = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Home",
        "👤 Register Student",
        "📷 Take Attendance",
        "📊 View Attendance"
    ]
)

# =========================================================
# HOME
# =========================================================

if option == "🏠 Home":

    st.header("Welcome 👋")

    st.write("""
    This application uses Artificial Intelligence and
    Face Recognition to automatically record student attendance.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registered Students", len(os.listdir(STUDENT_FOLDER)))

    with col2:
        if os.path.exists(ATTENDANCE_FILE):
            df = pd.read_csv(ATTENDANCE_FILE)
            st.metric("Attendance Records", len(df))
        else:
            st.metric("Attendance Records", 0)

    with col3:
        st.metric("Recognition", "AI")

    st.info(
        "Go to 'Register Student' first and add student face images."
    )


# =========================================================
# REGISTER STUDENT
# =========================================================

elif option == "👤 Register Student":

    st.header("👤 Register Student")

    student_name = st.text_input(
        "Enter Student Name"
    )

    uploaded_file = st.file_uploader(
        "Upload Student Face Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Image",
            width=300
        )

        if st.button("Register Student"):

            if student_name.strip() == "":
                st.error("Please enter student name.")

            else:

                image_array = np.array(image)

                faces = face_recognition.face_locations(
                    image_array
                )

                if len(faces) == 0:

                    st.error(
                        "No face detected. Please upload "
                        "a clear face image."
                    )

                elif len(faces) > 1:

                    st.error(
                        "Multiple faces detected. "
                        "Please upload an image containing "
                        "only one student."
                    )

                else:

                    filename = (
                        student_name.strip()
                        .replace(" ", "_")
                        + ".jpg"
                    )

                    save_path = os.path.join(
                        STUDENT_FOLDER,
                        filename
                    )

                    image.save(save_path)

                    st.success(
                        f"Student '{student_name}' registered successfully!"
                    )


# =========================================================
# TAKE ATTENDANCE
# =========================================================

elif option == "📷 Take Attendance":

    st.header("📷 Face Recognition Attendance")

    st.write(
        "Allow camera access and show the student's face."
    )

    known_encodings, known_names = load_known_faces()

    if len(known_encodings) == 0:

        st.warning(
            "No students registered yet. "
            "Please register students first."
        )

    else:

        camera_image = st.camera_input(
            "Take Student Photo"
        )

        if camera_image is not None:

            image = Image.open(camera_image)
            frame = np.array(image)

            face_locations = face_recognition.face_locations(
                frame
            )

            face_encodings = face_recognition.face_encodings(
                frame,
                face_locations
            )

            if len(face_encodings) == 0:

                st.error("No face detected.")

            else:

                recognized_students = []

                for face_encoding in face_encodings:

                    matches = face_recognition.compare_faces(
                        known_encodings,
                        face_encoding,
                        tolerance=0.5
                    )

                    face_distances = (
                        face_recognition.face_distance(
                            known_encodings,
                            face_encoding
                        )
                    )

                    if len(face_distances) > 0:

                        best_match_index = np.argmin(
                            face_distances
                        )

                        if matches[best_match_index]:

                            name = known_names[
                                best_match_index
                            ]

                            recognized_students.append(name)

                            marked = mark_attendance(name)

                            if marked:
                                st.success(
                                    f"✅ Attendance marked for {name}"
                                )
                            else:
                                st.info(
                                    f"ℹ️ {name}'s attendance "
                                    "is already marked today."
                                )

                        else:

                            st.warning(
                                "❌ Face not recognized."
                            )


# =========================================================
# VIEW ATTENDANCE
# =========================================================

elif option == "📊 View Attendance":

    st.header("📊 Attendance Records")

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)

        if len(df) > 0:

            st.dataframe(
                df,
                use_container_width=True
            )

            st.download_button(
                label="⬇️ Download Attendance CSV",
                data=df.to_csv(index=False),
                file_name="attendance.csv",
                mime="text/csv"
            )

        else:

            st.info("No attendance records available.")

    else:

        st.info("No attendance records available yet.")