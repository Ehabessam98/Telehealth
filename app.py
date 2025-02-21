import streamlit as st

# Title
st.title("COPD Telehealth Program - Rural to Remote Consultant Model")

# Sidebar for Patient Info
st.sidebar.header("Patient Information")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
age = st.sidebar.slider("Age", 40, 90, 65)
oxygen_level = st.sidebar.slider("Oxygen Saturation (%)", 70, 100, 95)
spirometry_value = st.sidebar.slider("Spirometry (FEV1 %)", 30, 100, 65)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 600, 350)
symptoms = st.sidebar.text_area("Symptoms", "Shortness of breath, fatigue")

# Display Patient Data
st.subheader(f"Patient: {patient_name}")
st.write(f"**Age:** {age}")
st.write(f"**Oxygen Level:** {oxygen_level}%")
st.write(f"**Spirometry (FEV1):** {spirometry_value}%")
st.write(f"**Peak Flow:** {peak_flow} L/min")
st.write(f"**Symptoms:** {symptoms}")

# Teleconsultation Process Simulation
st.subheader("Teleconsultation Process")
if st.button("Send Data to Remote Consultant"):
    st.success("Data sent to the chest consultant successfully!")
    st.info("Consultant is reviewing the data...")

    # Basic AI-driven interpretation (simulated)
    diagnosis = "Stable" if oxygen_level > 92 and spirometry_value > 50 else "Needs Immediate Attention"
    
    st.subheader("Consultant's Recommendation")
    if diagnosis == "Stable":
        st.success("Patient is stable. Continue current treatment and monitor regularly.")
    else:
        st.error("Patient requires immediate intervention! Consider medication adjustment or hospitalization.") 

st.write("**Workflow:** Rural hospital → Nurse collects data → Consultant reviews → Patient receives treatment plan.")

# Conclusion
st.subheader("Next Steps")
st.write("✅ Train nurses on telehealth devices.")
st.write("✅ Set up secure video consultation platform.")
st.write("✅ Establish a follow-up plan for COPD patients.")
