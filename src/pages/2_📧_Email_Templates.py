import streamlit as st
from datetime import datetime
from src.utils.enums import ScheduleStatus  # Ensure this import works
from src.utils.database import DatabaseManager
import os


db_manager = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )

# Streamlit App for Adding Templates
def main():
    st.title("Email Manager Dashboard")

    # Sidebar menu
    menu = ["Add Template", "View Templates"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Template":
        st.subheader("Add a New Email Template")

        # Input fields for template
        template_name = st.text_input("Template Name")
        template_body = st.text_area("Template Body")

        # Button to add template
        if st.button("Add Template"):
            if template_name and template_body:
                template_id = db_manager.add_template(template_name, template_body)
                st.success(f"Template added successfully! Template ID: {template_id}")
            else:
                st.error("Please provide both a template name and body.")

    elif choice == "View Templates":
        st.subheader("All Templates")
        templates = db_manager.get_all_templates()
        if templates:
            for template in templates:
                st.write(f"ID: {template[0]}")
                st.write(f"Name: {template[1]}")
                st.write(f"Body: {template[2]}")
                st.write("---")
        else:
            st.info("No templates found.")


if __name__ == "__main__":
    main()
