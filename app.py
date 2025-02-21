import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service_account.json"  # Your uploaded JSON file

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Your Google Sheets URL
SHEET_URL ="https://docs.google.com/spreadsheets/d/1SlogwnD9k-MTkCG1o-wwngsacp_ObovVIMobMd9Qo3Y/edit#gid=0"
  # Replace with your actual Google Sheets link
sheet = client.open_by_url(SHEET_URL).sheet1

# Streamlit UI
st.title("COPD Telehealth Program")

# Choose Role: GP or Consultant
role = st.sidebar.selectbox("Select Role", ["General Practitioner (GP)", "Consultant"])

if role == "General Practitioner (GP)":
    st.header("GP Interface - Enter Patient Data")

    # Patient Data Inputs
    patient_name = st.text_input("Patient Name")
    age = st.slider("Age", 1, 100, 40)
    oxygen_level = st.slider("Oxygen Saturation (%)", 70, 100, 95)
    spirometry_value = st.slider("Spirometry (FEV1 %)", 30, 100, 65)
    peak_flow = st.slider("Peak Flow (L/min)", 100, 600, 350)
    symptoms = st.text_area("Symptoms", "Shortness of breath, fatigue")

    if st.button("Send to Consultant"):
        new_data = [patient_name, age, oxygen_level, spirometry_value, peak_flow, symptoms, "", ""]
        sheet.append_row(new_data)
        st.success("Patient data sent to consultant!")

elif role == "Consultant":
    st.header("Consultant Interface - Review & Provide Feedback")

    # Fetch Data from Google Sheets
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        selected_patient = st.selectbox("Select a patient to review", df["Patient Name"])
        patient_data = df[df["Patient Name"] == selected_patient].iloc[0]

        st.write(f"**Age:** {patient_data['Age']}")
        st.write(f"**Oxygen Level:** {patient_data['Oxygen Level']}%")
        st.write(f"**Spirometry (FEV1):** {patient_data['Spirometry']}%")
        st.write(f"**Peak Flow:** {patient_data['Peak Flow']} L/min")
        st.write(f"**Symptoms:** {patient_data['Symptoms']}")

        # Consultant Feedback
        diagnosis = st.text_area("Diagnosis")
        recommendation = st.text_area("Recommendation")

        if st.button("Submit Feedback"):
            row_index = df[df["Patient Name"] == selected_patient].index[0] + 2  # Adjust for header row
            sheet.update_cell(row_index, 7, diagnosis)
            sheet.update_cell(row_index, 8, recommendation)
            st.success("Feedback submitted successfully!")

