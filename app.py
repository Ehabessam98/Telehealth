import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Load Google service account credentials from Streamlit secrets
service_account_info = st.secrets["google"]  # Already a dictionary, no need to parse
creds = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Google Sheets Setup
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SlogwnD9k-MTkCG1o-wwngsacp_ObovVIMobMd9Qo3Y/edit#gid=0"
sheet = client.open_by_url(SHEET_URL).sheet1

# Define Sheet Headers
headers = ["Patient Name", "Age", "Oxygen Level", "Spirometry", "Peak Flow", "Symptoms", "Diagnosis", "Recommendation"]

# Check if headers exist, if not, insert them
existing_data = sheet.get_all_values()
if not existing_data:
    sheet.insert_row(headers, 1)
elif existing_data[0] != headers:
    sheet.insert_row(headers, 1)

# Streamlit UI
st.title("COPD Telehealth Program")

# Choose Role: GP or Consultant
role = st.sidebar.selectbox("Select Role", ["General Practitioner (GP)", "Consultant"])

# 🔹 **GP Interface: Enter Patient Data**
if role == "General Practitioner (GP)":
    st.header("GP Interface - Enter Patient Data")

    # Patient Data Inputs
    patient_name = st.text_input("Patient Name")
    age = st.slider("Age", 1, 100, 40)
    oxygen_level = st.slider("Oxygen Saturation (%)", 70, 100, 95)
    spirometry_value = st.slider("Spirometry (FEV1 %)", 30, 100, 65)
    peak_flow = st.slider("Peak Flow (L/min)", 100, 600, 350)
    symptoms = st.text_area("Symptoms", "Shortness of breath, fatigue")

    # Submit Data to Google Sheets
    if st.button("Send to Consultant"):
        if patient_name:
            new_data = [patient_name, age, oxygen_level, spirometry_value, peak_flow, symptoms, "", ""]
            sheet.append_row(new_data)
            st.success("Patient data sent to consultant!")
        else:
            st.error("Please enter a patient name.")

# 🔹 **Consultant Interface: Review & Provide Feedback**
elif role == "Consultant":
    st.header("Consultant Interface - Review & Provide Feedback")

    # Fetch Data from Google Sheets
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        # Select Patient (Only show unique names for better UI)
        selected_patient = st.selectbox("Select a patient to review", df["Patient Name"].unique())

        # Fetch Latest Entry for the Selected Patient
        patient_data = df[df["Patient Name"] == selected_patient].iloc[-1]

        # Display Patient Information
        st.write(f"**Age:** {patient_data['Age']}")
        st.write(f"**Oxygen Level:** {patient_data['Oxygen Level']}%")
        st.write(f"**Spirometry (FEV1):** {patient_data['Spirometry']}%")
        st.write(f"**Peak Flow:** {patient_data['Peak Flow']} L/min")
        st.write(f"**Symptoms:** {patient_data['Symptoms']}")

        # Consultant Feedback Inputs
        diagnosis = st.text_area("Diagnosis")
        recommendation = st.text_area("Recommendation")

        # Submit Feedback & Update Google Sheets
        if st.button("Submit Feedback"):
            matching_rows = df[df["Patient Name"] == selected_patient].index
            if len(matching_rows) > 0:
                row_index = matching_rows[-1] + 2  # Updates the latest entry
                sheet.update_cell(row_index, 7, diagnosis)
                sheet.update_cell(row_index, 8, recommendation)
                st.success("Feedback submitted successfully!")
            else:
                st.error("Patient record not found!")
