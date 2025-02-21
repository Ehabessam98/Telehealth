import streamlit as st
import pandas as pd
import datetime
import os

# Title
st.title("🚑 COPD Telehealth Program - Rural to Remote Consultant Model")

# Sidebar for Patient Info
st.sidebar.header("📋 Patient Information")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
age = st.sidebar.slider("Age", 40, 90, 65)
oxygen_level = st.sidebar.slider("Oxygen Saturation (%)", 70, 100, 95)
spirometry_value = st.sidebar.slider("Spirometry (FEV1 %)", 30, 100, 65)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 600, 350)
symptoms = st.sidebar.text_area("Symptoms", "Shortness of breath, fatigue")

# Display Patient Data
st.subheader(f"🩺 Patient: {patient_name}")
st.write(f"**Age:** {age}")
st.write(f"**Oxygen Level:** {oxygen_level}%")
st.write(f"**Spirometry (FEV1):** {spirometry_value}%")
st.write(f"**Peak Flow:** {peak_flow} L/min")
st.write(f"**Symptoms:** {symptoms}")

# AI-Generated Consultant Feedback
st.subheader("📡 Teleconsultation Process")
if st.button("📤 Send Data to Remote Consultant"):
    st.success("✅ Data sent to the chest consultant successfully!")
    st.info("Consultant is reviewing the data...")

    # Diagnosis & Recommendation Logic
    if oxygen_level < 88 or spirometry_value < 50 or peak_flow < 200:
        diagnosis = "❌ Critical Condition - Immediate medical intervention needed!"
        recommendation = "Consider hospitalization, oxygen therapy, and medication adjustment."
    elif 88 <= oxygen_level <= 92 or 50 <= spirometry_value <= 65:
        diagnosis = "⚠ Moderate Condition - Close monitoring required!"
        recommendation = "Adjust medications, schedule regular follow-ups, and monitor oxygen levels daily."
    else:
        diagnosis = "✅ Stable Condition - Continue current treatment!"
        recommendation = "Maintain medications and follow-up as scheduled."
    
    st.subheader("📝 Consultant's Recommendation")
    st.write(f"**Diagnosis:** {diagnosis}")
    st.write(f"**Recommendation:** {recommendation}")
    
    # Save Data to CSV
    patient_record = {
        "Name": patient_name,
        "Age": age,
        "Oxygen Level": oxygen_level,
        "Spirometry": spirometry_value,
        "Peak Flow": peak_flow,
        "Symptoms": symptoms,
        "Diagnosis": diagnosis,
        "Recommendation": recommendation,
        "Timestamp": datetime.datetime.now()
    }

    file_path = "patient_records.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([patient_record])], ignore_index=True)
    else:
        df = pd.DataFrame([patient_record])
    
    df.to_csv(file_path, index=False)
    st.success("✅ Patient record saved successfully!")

# Display Past Records
st.subheader("📊 Patient History")
if os.path.exists("patient_records.csv"):
    df = pd.read_csv("patient_records.csv")
    st.dataframe(df.tail(5))
else:
    st.write("No patient records found.")

# Consultant Feedback Section
st.subheader("🩺 Consultant Feedback")
consultant_feedback = st.text_area("Enter Consultant's Feedback")
if st.button("💾 Save Feedback"):
    if consultant_feedback.strip():
        feedback_record = {"Consultant Feedback": consultant_feedback, "Timestamp": datetime.datetime.now()}
        feedback_df = pd.DataFrame([feedback_record])
        feedback_df.to_csv("consultant_feedback.csv", mode="a", header=not os.path.exists("consultant_feedback.csv"), index=False)
        st.success("Feedback saved successfully!")
    else:
        st.warning("Please enter some feedback before saving!")

st.write("**Workflow:** Rural hospital → Nurse collects data → Consultant reviews → Patient receives treatment plan.")
