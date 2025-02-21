if st.button("Send Data to Remote Consultant"):
    if not patient_name.strip() or not symptoms.strip() or not phone_number or not national_id:
        st.warning("⚠ Please fill in all required fields before submitting!")
    elif (not phone_number.isdigit() or len(phone_number) != 11 or not phone_number.startswith("0")) or \
         (not national_id.isdigit() or len(national_id) != 14 or national_id[0] not in ["2", "3"]):
        st.warning("⚠ Invalid phone number or national ID format.")
    else:
        submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Ensure it's always defined

        st.success("✅ Data sent successfully!")
        st.info("Consultant is reviewing the data...")

        # Save patient data to Google Sheets
        new_data = [patient_name, phone_number, national_id, submission_date, age, oxygen_level, spirometry_value, peak_flow, symptoms, "Pending"]
        worksheet.append_row(new_data)

        # Simulated Diagnosis & Recommendation
        diagnosis = "Stable" if oxygen_level > 92 and spirometry_value > 50 else "Needs Immediate Attention"
        st.subheader("💡 Consultant's Recommendation")
        if diagnosis == "Stable":
            st.success("✔ Patient is stable. Continue current treatment and monitor regularly.")
        else:
            st.error("⚠ Immediate intervention needed! Consider medication adjustment or hospitalization.")

# Ensure submission_date is defined before using it
if 'submission_date' not in locals():
    submission_date = "Not submitted"
