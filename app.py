import streamlit as st
from datetime import date
import json
import os

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Attendance Taker",
    page_icon="🎓",
    layout="centered"
)

# -----------------------------------
# FILE FOR STORING ATTENDANCE
# -----------------------------------

ATTENDANCE_FILE = "attendance.json"


# -----------------------------------
# LOAD ATTENDANCE DATA
# -----------------------------------

def load_attendance():

    if os.path.exists(ATTENDANCE_FILE):

        try:
            with open(ATTENDANCE_FILE, "r") as file:
                return json.load(file)

        except:
            return {}

    return {}


# -----------------------------------
# SAVE ATTENDANCE DATA
# -----------------------------------

def save_attendance(data):

    with open(ATTENDANCE_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------------
# ROLL NUMBERS
# -----------------------------------

roll_numbers = [
    "66", "67", "68", "69", "70",
    "71", "72", "73", "74", "75",
    "76", "77", "78", "79", "80",
    "81", "82", "83", "84", "85",
    "86", "87", "88", "89", "90",
    "91", "92", "93", "94", "95",
    "96", "97", "98", "99",

    "A0", "A1", "A2", "A3", "A4",
    "A5", "A6", "A7", "A8", "A9",

    "B0", "B1", "B2", "B3", "B4",
    "B5", "B6", "B7", "B8", "B9",

    "C0", "C1", "C2", "C3", "C4",
    "C5", "C6", "C7", "C8", "C9",

    "D0",

    "Ie6", "Ie7", "Ie8", "Ie9",
    "Ie10", "Ie11", "Ie12"
]


# -----------------------------------
# LOAD STORED DATA
# -----------------------------------

attendance_data = load_attendance()


# -----------------------------------
# SELECT DATE
# -----------------------------------

selected_date = st.date_input(
    "📅 Select Attendance Date",
    value=date.today(),
    format="DD/MM/YYYY"
)

date_key = selected_date.strftime("%d/%m/%Y")


# -----------------------------------
# LOAD ATTENDANCE FOR SELECTED DATE
# -----------------------------------

if "current_date" not in st.session_state:

    st.session_state.current_date = date_key

    st.session_state.absent_rolls = set(
        attendance_data.get(date_key, [])
    )


elif st.session_state.current_date != date_key:

    st.session_state.current_date = date_key

    st.session_state.absent_rolls = set(
        attendance_data.get(date_key, [])
    )


st.info(
    f"📅 Attendance Date: **{date_key}**"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.markdown(
    """
    <h1 style="text-align:center;">
    🎓 AI Attendance Taker
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center;">
    Click the roll numbers of absent students
    </p>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# ATTENDANCE SECTION
# -----------------------------------

st.markdown("---")

st.markdown("### 📝 Mark Attendance")

st.write(
    "Click a roll number to mark that student as **ABSENT**. "
    "Students who are not selected are considered **PRESENT**."
)


# -----------------------------------
# ROLL NUMBER BUTTONS
# -----------------------------------

columns = 5

for i in range(0, len(roll_numbers), columns):

    cols = st.columns(columns)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(roll_numbers):

            roll = roll_numbers[index]

            with col:

                if roll in st.session_state.absent_rolls:

                    if st.button(
                        f"❌ {roll}",
                        key=f"absent_{roll}",
                        use_container_width=True
                    ):

                        # Remove from absent list
                        st.session_state.absent_rolls.remove(roll)

                        # Save updated attendance
                        attendance_data[date_key] = list(
                            st.session_state.absent_rolls
                        )

                        save_attendance(attendance_data)

                        st.rerun()

                else:

                    if st.button(
                        roll,
                        key=f"present_{roll}",
                        use_container_width=True
                    ):

                        # Add to absent list
                        st.session_state.absent_rolls.add(roll)

                        # Save updated attendance
                        attendance_data[date_key] = list(
                            st.session_state.absent_rolls
                        )

                        save_attendance(attendance_data)

                        st.rerun()


# -----------------------------------
# ATTENDANCE SUMMARY
# -----------------------------------

st.markdown("---")

st.markdown("### 📊 Attendance Summary")


total_students = len(roll_numbers)

total_absent = len(
    st.session_state.absent_rolls
)

total_present = (
    total_students - total_absent
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Students",
        total_students
    )


with col2:

    st.metric(
        "✅ Total Present",
        total_present
    )


with col3:

    st.metric(
        "❌ Total Absent",
        total_absent
    )


# -----------------------------------
# ABSENT STUDENTS
# -----------------------------------

st.markdown("### ❌ Absent Students")


if total_absent == 0:

    st.success(
        "🎉 No students are marked absent."
    )

else:

    # Keep original roll-number order
    absent_list = [
        roll
        for roll in roll_numbers
        if roll in st.session_state.absent_rolls
    ]

    st.warning(
        "Absent Roll Numbers: "
        + ", ".join(absent_list)
    )


# -----------------------------------
# PRESENT STUDENTS
# -----------------------------------

st.markdown("### ✅ Present Students")


present_rolls = [
    roll
    for roll in roll_numbers
    if roll not in st.session_state.absent_rolls
]


st.success(
    "Present Roll Numbers: "
    + ", ".join(present_rolls)
)


# -----------------------------------
# ATTENDANCE PERCENTAGE
# -----------------------------------

if total_students > 0:

    present_percentage = (
        total_present / total_students
    ) * 100

    st.progress(
        int(present_percentage),
        text=f"Class Attendance: {present_percentage:.2f}%"
    )


# -----------------------------------
# AI ASSISTANT
# -----------------------------------

st.markdown("---")

st.markdown("### 🤖 AI Attendance Assistant")


if total_absent == 0:

    st.success(
        "🎉 Excellent! All students are present today."
    )

elif total_present >= total_students * 0.75:

    st.info(
        f"👍 Good attendance today. "
        f"{total_present} students are present and "
        f"{total_absent} students are absent."
    )

else:

    st.warning(
        f"⚠️ Attendance is low today. "
        f"{total_present} students are present and "
        f"{total_absent} students are absent."
    )


# -----------------------------------
# RESET CURRENT DATE
# -----------------------------------

st.markdown("---")

if st.button(
    "🔄 Reset This Date",
    use_container_width=True
):

    st.session_state.absent_rolls = set()

    # Save empty attendance for this date
    attendance_data[date_key] = []

    save_attendance(attendance_data)

    st.rerun()


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "🎓 AI Attendance Taker | "
    "Smart Classroom Attendance System"
)