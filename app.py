import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Set page configuration
st.set_page_config(page_title="COPD Telehealth", layout="wide")

# Load Google Sheets credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1SlogwnD9k-MTkCG1o-wwngsacp_ObovVIMobMd9Qo3Y/edit#gid=0")
worksheet = spreadsheet.sheet1

# Customizing the style
st.markdown(
    """
    <style>
    body { background-color: #F5E8C7; }
    .stButton>button { background-color: #E67E22; color: white; border-radius: 8px; width: 100%; }
    .stSuccess { color: green; }
    .stError { color: red; }
    .css-1cpxqw2 { background-color: #F4D03F !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with styling
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>COPD Telehealth Program</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #D35400;'>Rural to Remote Consultant Model</h2>", unsafe_allow_html=True)

# Sidebar for Patient Info
st.sidebar.header("🩺 Patient Information")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
age = st.sidebar.slider("Age", 40, 90, 65)
oxygen_level = st.sidebar.slider("Oxygen Saturation (%)", 70, 100, 95)
spirometry_value = st.sidebar.slider("Spirometry (FEV1 %)", 30, 100, 65)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 600, 350)
symptoms = st.sidebar.text_area("Symptoms", "Shortness of breath, fatigue")

# Main layout
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("👤 Patient Details")
    st.info(f"**Name:** {patient_name}")
    st.write(f"**Age:** {age}")
    st.write(f"**Oxygen Level:** {oxygen_level}%")
    st.write(f"**Spirometry (FEV1):** {spirometry_value}%")
    st.write(f"**Peak Flow:** {peak_flow} L/min")
    st.write(f"**Symptoms:** {symptoms}")

# Severity Assessment
def assess_severity(oxygen, fev1):
    if oxygen < 90 or fev1 < 50:
        return "🔴 High Risk - Needs Urgent Attention!", "danger"
    elif 90 <= oxygen <= 94 or 50 <= fev1 < 70:
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

# Teleconsultation Process
st.subheader("📞 Teleconsultation Process")
if st.button("Send Data to Remote Consultant"):
    st.success("✅ Data sent successfully!")
    st.info("Consultant is reviewing the data...")

    # Save patient data to Google Sheets
    new_data = [patient_name, age, oxygen_level, spirometry_value, peak_flow, symptoms, severity_message]
    worksheet.append_row(new_data)

    # Simulated Diagnosis & Recommendation
    diagnosis = "Stable" if oxygen_level > 92 and spirometry_value > 50 else "Needs Immediate Attention"
    
    st.subheader("💡 Consultant's Recommendation")
    if diagnosis == "Stable":
        st.success("✔ Patient is stable. Continue current treatment and monitor regularly.")
    else:
        st.error("⚠ Immediate intervention needed! Consider medication adjustment or hospitalization.")

st.write("**Workflow:** 🏥 Rural hospital → 🩺 Nurse collects data → 👨‍⚕️ Consultant reviews → 🏠 Patient receives treatment plan.")

# Next Steps
st.subheader("✅ Next Steps")
st.write("✔ Train nurses on telehealth devices.")
st.write("✔ Set up secure video consultation platform.")
st.write("✔ Establish a follow-up plan for COPD patients.")

# Option to Download Report
patient_data = {
    "Name": [patient_name],
    "Age": [age],
    "Oxygen Level (%)": [oxygen_level],
    "Spirometry (FEV1 %)": [spirometry_value],
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
