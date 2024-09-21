from datetime import datetime
import streamlit as st
from src.utils.database import DatabaseManager
# from src.utils.helpers import humanize_date
from src.utils.enums import ScheduleStatus

import os


db = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )

def get_status_color(status):
    return {
        ScheduleStatus.PENDING: "blue",
        ScheduleStatus.SENT: "green",
        ScheduleStatus.FAILED: "red",
        ScheduleStatus.CANCELLED: "gray"
    }.get(status, "black")

def display_schedule(schedule):
    schedule_date = schedule[2]
    status = schedule[3] #get("status", ScheduleStatus.PENDING)
    status_color = get_status_color(status)
    
    with st.expander(f"Schedule for {schedule_date} - Status: {status}"):
        email = db.get_sent_email(schedule[1])
        if email:
            sent_date = email[4]
            st.write(f"**Subject**: {email[2]}")
            st.write(f"**Recipients**: {', '.join(email[1])}")
            st.write(f"**Sent Date**: {sent_date}")
            st.text_area("Email Body", value=email[3], height=200, disabled=True, key=f"email_body_{schedule[1]}")
        else:
            st.warning("Email not found.")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(f"**Scheduled Date**: {schedule_date}")
        
        new_date = col2.date_input("New Date", value=datetime.fromisoformat(f"{schedule_date}").date(), key=f"date_{schedule[1]}")
        new_time = col3.time_input("New Time", value=datetime.fromisoformat(f"{schedule_date}").time(), key=f"time_{schedule[1]}")
        
        if col4.button("Update", key=f"update_{schedule[0]}"):
            new_datetime = datetime.combine(new_date, new_time)
            db.update_schedule(schedule[0], scheduled_date=new_datetime.isoformat())
            st.success("Schedule updated successfully")
            st.experimental_rerun()

        if col5.button("Delete", key=f"delete_{schedule[0]}"):
            db.delete_schedule(schedule[0])
            st.success("Schedule deleted successfully")
            st.experimental_rerun()

def main():
    st.title("Schedules")

    # Get all schedules
    schedules = db.get_all_schedules()

    # Display existing schedules
    if not schedules:
        st.info("No schedules found.")
    else:
        for schedule in schedules:
            display_schedule(schedule)

    # Add new schedule
    st.header("Add New Schedule")
    with st.form("add_schedule_form"):
        sent_emails = db.get_all_sent_emails()
        email_options = [(email[0], f"{email[4]} - {email[2]}") for email in sent_emails]
        selected_email = st.selectbox("Select Email", email_options, format_func=lambda x: x[1], key="email_id")
        schedule_date = st.date_input("Schedule Date")
        schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
        initial_status = st.selectbox("Initial Status", options=list(ScheduleStatus), format_func=lambda x: x.value)
        submit_button = st.form_submit_button("Add Schedule")

    if submit_button:
        if selected_email and schedule_date and schedule_time:
            email_id = selected_email[0]
            schedule_datetime = datetime.combine(schedule_date, schedule_time)
            db.add_schedule(email_id=email_id, scheduled_date=schedule_datetime.isoformat(), status=initial_status)
            st.success("Schedule added successfully")
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields")

if __name__ == "__main__":
    main()

# from datetime import datetime
# import streamlit as st
# from src.utils.db import DatabaseManager
# # from src.utils.helpers import humanize_date
# from src.utils.enums import ScheduleStatus

# # Initialize the DatabaseManager
# db = DatabaseManager()

# def get_status_color(status):
#     return {
#         ScheduleStatus.PENDING: "blue",
#         ScheduleStatus.SENT: "green",
#         ScheduleStatus.FAILED: "red",
#         ScheduleStatus.CANCELLED: "gray"
#     }.get(status, "black")

# def main():
#     st.title("Schedules")
#     # Get all schedules
#     schedules = db.get_all_schedules()
    
#     # Display existing schedules
#     if not schedules:
#         st.info("No schedules found.")
#     else:
#         for schedule in schedules:
#             schedule_date = schedule["scheduled_date"]
#             status = schedule.get("status", ScheduleStatus.PENDING)
#             status_color = get_status_color(status)
#             with st.expander(f"Schedule for {schedule_date} - Status: {status_color} [{status}]"):
#                 email = db.get_sent_email(schedule["email_id"])
#                 if email:
#                     sent_date = email["sent_date"]
                    
#                 else:
#                     for schedule in schedules:
#                         schedule_date = humanize_date(schedule["scheduled_date"])
#                         status = ScheduleStatus.PENDING
#                         status_color = get_status_color(status)

#                         with db.get_sent_email(email_id) as email:
#                             sent_date = humanize_date(email["sent_date"])
#                             st.write(f"{email['subject']}", key="subject")
#                             st.write(", ".join(email['recipients']), key="recipients")
#                             st.write(f"{sent_date}", key="sent_date")
#                             st.text_area("", value=email["body"], height=200, key="body", schedule_doc_id=email["schedule_doc_id"], disabled=True)

#                         col1, col2, col3, col4, col5 = st.columns(5)
#                         with col1:
#                             value_datetime = humanize_date(schedule["scheduled_date"], date)
#                             st.write(value_datetime, key=f"time__{schedule['doc_id']}")
#                         with col2:
#                             new_time = col2.time_input(
#                                 value=datetime.fromisformat(schedule["scheduled_date"]).time(),
#                                 key=f"time__{schedule['doc_id']}"
#                             )
#                         if col4_button("Update", key=f"update_{schedule_doc_id}", use_container_width=True):
#                             new_datetime = datetime.combine(new_date, new_time)
#                             db.update_schedule(schedule_doc_id, new_datetime)
#                             st.success("Update schedule successfully")
#                             st.experimental_rerun()

#                         if col5_button("Delete", key=f"delete_{schedule_doc_id}", use_container_width=True):
#                             db.delete_schedule(schedule_doc_id)
#                             st.success("Schedule deleted successfully")
#                             st.experimental_rerun()

# # Add new schedule
# st.header("Add New Schedule")
# with st.form("add_schedule_form"):
#     sent_emails = db.get_all_sent_emails()
#     email_options = [(email.doc_id, f"{email.sent_date} - {email.subject}") for email in sent_emails]
#     selected_email = st.selectbox("Select Email", email_options, key="email_id")
#     schedule_date = st.date_input("Schedule Date")
#     schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
#     initial_status = st.selectbox("Initial Status", options=ScheduleStatus.list(), index=0)
#     submit_button = st.form_submit_button("Add Schedule")

# if submit_button:
#     if selected_email and schedule_date and schedule_time:
#         email_id = email_options[selected_email][0]
#         schedule_datetime = datetime.combine(schedule_date, schedule_time)
#         db.add_schedule(email_id, schedule_datetime, initial_status)
#         st.success("Schedule added successfully")
#         st.experimental_rerun()
#     else:
#         st.error("Please fill in all fields")

# if _name_ == "_main_":
#     main()
                    
                    


