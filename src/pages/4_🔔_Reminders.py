import streamlit as st
from datetime import datetime
import streamlit as st
from src.utils.database import DatabaseManager
import os


db = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )

def main():
    st.title("🔔 Reminders")

    # Get all reminders
    reminders = db.get_all_reminders()

    # Display existing reminders
    st.header("Existing Reminders")

    if not reminders:
        st.info("No reminders found.")
    else:
        for reminder in reminders:
            with st.expander(f"Reminder for {reminder[3]}"):
                email = db.get_sent_email(reminder[1])
                if email:
                    st.write(f"**Subject:** {email[2]}")
                    st.write(f"**Recipients:** {', '.join(email[1])}")
                    st.write(f"**Sent Date:** {email[4]}")
                    st.write("**Email Body:**")
                    st.text_area("", value=email[3], height=100, key=f"body_{reminder[1]}", disabled=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_date = st.date_input("Reschedule reminder", value=datetime.fromisoformat(f"{reminder[3]}").date(), key=f"reschedule_date_{reminder[1]}")
                    new_time = st.time_input("", value=datetime.fromisoformat(f"{reminder[3]}").time(), key=f"reschedule_time_{reminder[1]}")
                    
                    if st.button("Update", key=f"update_{reminder[1]}"):
                        new_datetime = datetime.combine(new_date, new_time)
                        db.update_reminder(reminder[1], new_datetime)
                        st.success("Reminder updated successfully")
                        st.experimental_rerun()
                
                with col2:
                    if st.button("Delete", key=f"delete_{reminder[1]}"):
                        db.delete_reminder(reminder[1])
                        st.success("Reminder deleted successfully")
                        st.experimental_rerun()
    
    # Add new reminder
    st.header("Add New Reminder")
    with st.form("add_reminder_form"):
        sent_emails = db.get_all_sent_emails()
        email_options = {f"{email[2]} ({email[4]})": email[0] for email in sent_emails}
        
        selected_email = st.selectbox("Select Email", options=list(email_options.keys()))
        reminder_date = st.date_input("Reminder Date", min_value=datetime.now().date())
        reminder_time = st.time_input("Reminder Time", value=datetime.now().time())
        
        submit_button = st.form_submit_button("Add Reminder")
        
        if submit_button:
            if selected_email and reminder_date and reminder_time:
                reminder_datetime = datetime.combine(reminder_date, reminder_time)
                email_id = email_options[selected_email]
                db.add_reminder(email_id, reminder_datetime)
                st.success("Reminder added successfully!")
                st.experimental_rerun()
            else:
                st.error("Please fill in all fields")

if __name__ == "__main__":
    main()
