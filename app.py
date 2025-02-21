import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="COPD Telehealth", layout="wide")

# Load Google Sheets credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1SlogwnD9k-MTkCG1o-wwngsacp_ObovVIMobMd9Qo3Y/edit#gid=0")
    worksheet = spreadsheet.sheet1
except Exception:
    st.error("🚨 Error: Unable to authenticate with Google Sheets. Check your credentials.")
    st.stop()

# Title and Header
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>COPD Telehealth Program</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #D35400;'>Rural to Remote Consultant Model</h2>", unsafe_allow_html=True)

# Sidebar for Patient Info
st.sidebar.header("🩺 Patient Information")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
phone_number = st.sidebar.text_input("Phone Number (11 digits starting with 0)")
national_id = st.sidebar.text_input("National ID (14 digits starting with 2 or 3)")
age = st.sidebar.slider("Age", 20, 90, 65)
oxygen_level = st.sidebar.slider("Oxygen Saturation (%)", 70, 100, 95)
spirometry_value = st.sidebar.slider("Spirometry (FEV1 % Predicted)", 30, 100, 65)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 600, 350)
symptoms = st.sidebar.text_area("Symptoms", "Shortness of breath, fatigue")

# Validate phone number
if phone_number and (not phone_number.isdigit() or len(phone_number) != 11 or not phone_number.startswith("0")):
    st.sidebar.error("⚠ Invalid phone number. Must be 11 digits starting with 0.")

# Validate national ID
if national_id and (not national_id.isdigit() or len(national_id) != 14 or national_id[0] not in ["2", "3"]):
    st.sidebar.error("⚠ Invalid National ID. Must be 14 digits starting with 2 or 3.")

# Main layout
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("👤 Patient Details")
    st.info(f"**Name:** {patient_name}")
    st.write(f"**Phone Number:** {phone_number}")
    st.write(f"**National ID:** {national_id}")
    st.write(f"**Age:** {age}")
    st.write(f"**Oxygen Level:** {oxygen_level}%")
    st.write(f"**Spirometry (FEV1 % Predicted):** {spirometry_value}%")
    st.write(f"**Peak Flow:** {peak_flow} L/min")
    st.write(f"**Symptoms:** {symptoms}")

# Severity Assessment
def assess_severity(oxygen, fev1):
    if oxygen < 88 or fev1 < 50:
        return "🔴 High Risk - Needs Urgent Attention!", "danger"
    elif 88 <= oxygen <= 92 or 50 <= fev1 < 80:
        return "🟠 Moderate Risk - Requires Monitoring.", "warning"
    else:
        return "🟢 Low Risk - Stable Condition.", "success"

severity_message, severity_status = assess_severity(oxygen_level, spirometry_value)

with col2:
    st.subheader("📊 Severity Assessment")
    if severity_status == "danger":
        st.error(severity_message)
    elif severity_status == "warning":
        st.warning(severity_message)
    else:
        st.success(severity_message)

# Initialize submission_date with a default value
submission_date = "Not Submitted"

# Teleconsultation Process
st.subheader("📞 Teleconsultation Process")
if st.button("Send Data to Remote Consultant"):
    if not patient_name.strip() or not symptoms.strip() or not phone_number or not national_id:
        st.warning("⚠ Please fill in all required fields before submitting!")
    elif (not phone_number.isdigit() or len(phone_number) != 11 or not phone_number.startswith("0")) or \
         (not national_id.isdigit() or len(national_id) != 14 or national_id[0] not in ["2", "3"]):
        st.warning("⚠ Invalid phone number or national ID format.")
    else:
        submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("✅ Data sent successfully!")
        st.info("Consultant is reviewing the data...")

        # Save patient data to Google Sheets
        new_data = [patient_name, phone_number, national_id, submission_date, age, oxygen_level, spirometry_value, peak_flow, symptoms, severity_message, "Pending"]
        worksheet.append_row(new_data)

        # Simulated Diagnosis & Recommendation
        diagnosis = "Stable" if oxygen_level > 92 and spirometry_value > 50 else "Needs Immediate Attention"
        st.subheader("💡 Consultant's Recommendation")
        if diagnosis == "Stable":
            st.success("✔ Patient is stable. Continue current treatment and monitor regularly.")
        else:
            st.error("⚠ Immediate intervention needed! Consider medication adjustment or hospitalization.")

st.write("**Workflow:** 🏥 Rural hospital → 🩺 Nurse collects data → 👨‍⚕️ Consultant reviews → 🏠 Patient receives treatment plan.")

# Option to Download Report
patient_data = {
    "Name": [patient_name],
    "Phone Number": [phone_number],
    "National ID": [national_id],
    "Submission Date": [submission_date],  # Now always defined
    "Age": [age],
    "Oxygen Level (%)": [oxygen_level],
    "Spirometry (FEV1 % Predicted)": [spirometry_value],
    "Peak Flow (L/min)": [peak_flow],
    "Symptoms": [symptoms],
    "Risk Assessment": [severity_message]
}

df = pd.DataFrame(patient_data)

st.download_button(
    label="📥 Download Patient Report (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name=f"{patient_name}_COPD_Report.csv",
    mime="text/csv",
)
