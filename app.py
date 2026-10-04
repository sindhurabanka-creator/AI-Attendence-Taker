import streamlit as st
from datetime import date

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI Attendance Taker",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.attendance-card {
    padding: 25px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.result {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="title">🤖 AI Attendance Taker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart and Simple Daily Attendance System</div>',
    unsafe_allow_html=True
)


# -----------------------------
# SESSION STATE
# -----------------------------
if "attendance" not in st.session_state:
    st.session_state.attendance = []

if "message" not in st.session_state:
    st.session_state.message = ""


# -----------------------------
# STUDENT DETAILS
# -----------------------------
st.markdown("### 👤 Student Details")

name = st.text_input(
    "Enter Student Name",
    placeholder="Example: Sindhura"
)

today = date.today()

st.info(f"📅 Today's Date: {today.strftime('%d-%m-%Y')}")


# -----------------------------
# ATTENDANCE SECTION
# -----------------------------
st.markdown("### 📝 Mark Your Attendance")

col1, col2 = st.columns(2)

with col1:
    present_button = st.button(
        "✅ PRESENT",
        use_container_width=True
    )

with col2:
    absent_button = st.button(
        "❌ ABSENT",
        use_container_width=True
    )


# -----------------------------
# PRESENT BUTTON
# -----------------------------
if present_button:

    if name.strip() == "":
        st.warning("⚠️ Please enter your name first.")

    else:
        attendance_record = {
            "Name": name,
            "Date": today.strftime("%d-%m-%Y"),
            "Status": "Present"
        }

        st.session_state.attendance.append(attendance_record)

        st.success("✅ Your attendance is marked PRESENT.")


# -----------------------------
# ABSENT BUTTON
# -----------------------------
if absent_button:

    if name.strip() == "":
        st.warning("⚠️ Please enter your name first.")

    else:
        attendance_record = {
            "Name": name,
            "Date": today.strftime("%d-%m-%Y"),
            "Status": "Absent"
        }

        st.session_state.attendance.append(attendance_record)

        st.error("❌ Your attendance is marked ABSENT.")


# -----------------------------
# ATTENDANCE STATISTICS
# -----------------------------
st.markdown("---")

st.markdown("### 📊 Attendance Statistics")

total_days = len(st.session_state.attendance)

present_days = sum(
    1 for record in st.session_state.attendance
    if record["Status"] == "Present"
)

absent_days = sum(
    1 for record in st.session_state.attendance
    if record["Status"] == "Absent"
)


if total_days > 0:
    percentage = (present_days / total_days) * 100
else:
    percentage = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Days",
        total_days
    )

with col2:
    st.metric(
        "Present",
        present_days
    )

with col3:
    st.metric(
        "Absent",
        absent_days
    )


st.progress(
    int(percentage),
    text=f"Attendance Percentage: {percentage:.2f}%"
)


# -----------------------------
# ATTENDANCE HISTORY
# -----------------------------
st.markdown("---")

st.markdown("### 📋 Attendance History")

if len(st.session_state.attendance) > 0:

    for record in reversed(st.session_state.attendance):

        if record["Status"] == "Present":

            st.success(
                f"📅 {record['Date']} | "
                f"👤 {record['Name']} | "
                f"✅ {record['Status']}"
            )

        else:

            st.error(
                f"📅 {record['Date']} | "
                f"👤 {record['Name']} | "
                f"❌ {record['Status']}"
            )

else:

    st.info("No attendance records yet.")


# -----------------------------
# AI ASSISTANT MESSAGE
# -----------------------------
st.markdown("---")

st.markdown("### 🤖 AI Attendance Assistant")

if total_days == 0:

    st.info(
        "Hello! 👋 Please mark your attendance to start "
        "tracking your attendance."
    )

elif percentage >= 75:

    st.success(
        f"🎉 Good job! Your attendance is {percentage:.2f}%. "
        "You are maintaining good attendance."
    )

else:

    st.warning(
        f"⚠️ Your attendance is {percentage:.2f}%. "
        "Please try to attend more classes."
    )


# -----------------------------
# RESET BUTTON
# -----------------------------
st.markdown("---")

if st.button(
    "🔄 Reset Attendance",
    use_container_width=True
):

    st.session_state.attendance = []
    st.session_state.message = ""

    st.rerun()