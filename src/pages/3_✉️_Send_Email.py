import streamlit as st
from datetime import datetime, timedelta
from src.utils.database import DatabaseManager
import os
# Initialize the DatabaseManager
db = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )

def main():
    st.title("✉️ Send Email")

    # Get all profiles and templates
    profiles = db.get_all_profiles()
    templates = db.get_all_templates()

    # Select recipients
    selected_profiles = st.multiselect(
        "Select Recipients",
        options=[p[1] for p in profiles],
        format_func=lambda x: f"{x} ({next(p[4] for p in profiles if p[1] == x)})"
    )

    # Select template
    selected_template = st.selectbox("Select Template", options=[t[1] for t in templates])

    # Toggle for signature
    add_signature = st.checkbox("Add Signature")  # Changed from toggle to checkbox

    # Get the selected template body
    if templates:
        template_body = next(t[2] for t in templates if t[1] == selected_template)
    else:
        template_body = ""

    # Get user profile for signature
    user_profile = db.get_user_profile()  # Removed duplicate call
    signature = user_profile.get("signature", "") if user_profile else ""

    # Display email content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Raw Email Body")
        st.text_area("", value=template_body, height=300, key="raw_email")

    with col2:
        st.subheader("Email Preview")
        preview_body = template_body
        if add_signature:
            preview_body += f"\n\n{signature}"
        st.text_area("", value=preview_body, height=300, key="preview_email")

    # Send, Schedule, and Reminder buttons
    col1, col2, col3 = st.columns(3)  # Removed the duplicate columns declaration

    with col1:
        if st.button("Send Now", use_container_width=True):
            if selected_profiles and selected_template:
                for profile in selected_profiles:
                    recipient_email = next(p[4] for p in profiles if p[1] == profile)
                    email_id = db.add_sent_email(
                        recipient_email, f"Email to {profile}", preview_body, datetime.now()
                    )
                    db.add_schedule(email_id, datetime.now())
                st.success("Emails scheduled for immediate sending")
            else:
                st.error("Please select at least one recipient and a template")

    with col2:
        schedule_date = st.date_input("Schedule Date")
        schedule_time = st.time_input("Schedule Time")
        if st.button("Schedule", use_container_width=True):
            if selected_profiles and selected_template:
                scheduled_datetime = datetime.combine(schedule_date, schedule_time)
                for profile in selected_profiles:
                    recipient_email = next(p[4] for p in profiles if p[1] == profile)
                    email_id = db.add_sent_email(
                        recipient_email, f"Email to {profile}", preview_body, sent_date=scheduled_datetime
                    )
                    db.add_schedule(email_id, scheduled_datetime)
                st.success(f"Emails scheduled for {scheduled_datetime}")
            else:
                st.error("Please select at least one recipient and a template")

    with col3:
        reminder_title = st.text_input("Reminder Title", value="Send Email")
        reminder_days = st.number_input("Reminder (days from now):", min_value=1, value=1)
        
        if st.button("Add Reminder", use_container_width=True):
            if selected_profiles and selected_template:
                reminder_date = datetime.now() + timedelta(days=reminder_days)
                
                for profile in selected_profiles:
                    recipient_email = next(p[4] for p in profiles if p[1] == profile)
                    email_id = db.add_sent_email(recipient_email, f"Email to {profile}", preview_body, datetime.now())
                    db.add_reminder(email_id, reminder_title, reminder_date)
                
                st.success(f"Reminders set for {reminder_date}")
            else:
                st.error("Please select at least one recipient and a template")

if __name__ == "__main__":
    main()

