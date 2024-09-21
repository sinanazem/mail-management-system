import json
import psycopg2
from psycopg2 import sql
from datetime import datetime
from src.utils.enums import ScheduleStatus
import os

class DatabaseManager:
    def __init__(self, dbname, user, password, host=os.getenv("POSTGRES_HOST"), port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id SERIAL PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                profession TEXT,
                email TEXT,
                about TEXT,
                twitter TEXT,
                github TEXT,
                linkedin TEXT,
                personal_website TEXT,
                instagram TEXT,
                profile_image_path TEXT
            );
            CREATE TABLE IF NOT EXISTS templates (
                id SERIAL PRIMARY KEY,
                name TEXT,
                body TEXT
            );
            CREATE TABLE IF NOT EXISTS sent_emails (
                id SERIAL PRIMARY KEY,
                recipients TEXT,
                subject TEXT,
                body TEXT,
                sent_date TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id SERIAL PRIMARY KEY,
                email_id INTEGER,
                title TEXT,
                reminder_date TIMESTAMP,
                FOREIGN KEY (email_id) REFERENCES sent_emails (id)
            );
            CREATE TABLE IF NOT EXISTS schedules (
                id SERIAL PRIMARY KEY,
                email_id INTEGER,
                scheduled_date TIMESTAMP,
                status TEXT,
                FOREIGN KEY (email_id) REFERENCES sent_emails (id)
            );
            CREATE TABLE IF NOT EXISTS user_profile (
                id SERIAL PRIMARY KEY,
                data JSONB
            );
            """
        )
        self.conn.commit()

    # Helper method for running updates
    def _update(self, table, doc_id, **fields):
        set_values = ', '.join([f"{k} = %s" for k in fields.keys()])
        query = sql.SQL(f"UPDATE {table} SET {set_values} WHERE id = %s")
        self.cursor.execute(query, (*fields.values(), doc_id))
        self.conn.commit()

    # Profile management
    def add_profile(self, first_name, last_name, profession, email, about, twitter, github, linkedin, personal_website, instagram, profile_image_path):
        self.cursor.execute(
            """
            INSERT INTO profiles (first_name, last_name, profession, email, about, twitter, github, linkedin, personal_website, instagram, profile_image_path) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id
            """,
            (first_name, last_name, profession, email, about, twitter, github, linkedin, personal_website, instagram, profile_image_path)
        )
        profile_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return profile_id

    def get_profile(self, profile_id):
        self.cursor.execute("SELECT * FROM profiles WHERE id = %s", (profile_id,))
        return self.cursor.fetchone()

    def update_profile(self, profile_id, **fields):
        self._update('profiles', profile_id, **fields)

    def delete_profile(self, profile_id):
        self.cursor.execute("DELETE FROM profiles WHERE id = %s", (profile_id,))
        self.conn.commit()

    def get_all_profiles(self):
        self.cursor.execute("SELECT * FROM profiles")
        return self.cursor.fetchall()

    # Template management
    def add_template(self, name, body):
        self.cursor.execute(
            """
            INSERT INTO templates (name, body) 
            VALUES (%s, %s) 
            RETURNING id
            """,
            (name, body)
        )
        template_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return template_id

    def get_template(self, template_id):
        self.cursor.execute("SELECT * FROM templates WHERE id = %s", (template_id,))
        return self.cursor.fetchone()

    def update_template(self, template_id, **fields):
        self._update('templates', template_id, **fields)

    def delete_template(self, template_id):
        self.cursor.execute("DELETE FROM templates WHERE id = %s", (template_id,))
        self.conn.commit()

    def get_all_templates(self):
        self.cursor.execute("SELECT * FROM templates")
        return self.cursor.fetchall()

    # Sent emails management
    def add_sent_email(self, recipients, subject, body, sent_date):
        sent_date_str = sent_date.isoformat()
        self.cursor.execute(
            """
            INSERT INTO sent_emails (recipients, subject, body, sent_date) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id
            """,
            (recipients, subject, body, sent_date_str)
        )
        email_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return email_id

    def get_sent_email(self, email_id):
        self.cursor.execute("SELECT * FROM sent_emails WHERE id = %s", (email_id,))
        return self.cursor.fetchone()

    def get_all_sent_emails(self):
        self.cursor.execute("SELECT * FROM sent_emails")
        return self.cursor.fetchall()

    # Reminder management
    def add_reminder(self, email_id, reminder_title, reminder_date):
        reminder_date_str = reminder_date.isoformat()
        self.cursor.execute(
            """
            INSERT INTO reminders (email_id, title, reminder_date) 
            VALUES (%s, %s, %s) 
            RETURNING id
            """,
            (email_id, reminder_title, reminder_date_str)
        )
        reminder_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return reminder_id

    def get_reminder(self, reminder_id):
        self.cursor.execute("SELECT * FROM reminders WHERE id = %s", (reminder_id,))
        return self.cursor.fetchone()

    def update_reminder(self, reminder_id, **fields):
        self._update('reminders', reminder_id, **fields)

    def delete_reminder(self, reminder_id):
        self.cursor.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
        self.conn.commit()

    def get_all_reminders(self):
        self.cursor.execute("SELECT * FROM reminders")
        return self.cursor.fetchall()

    # Schedule management
    def add_schedule(self, email_id, scheduled_date, status=ScheduleStatus.PENDING.value):
        scheduled_date_str = scheduled_date.isoformat()
        self.cursor.execute(
            """
            INSERT INTO schedules (email_id, scheduled_date, status) 
            VALUES (%s, %s, %s) 
            RETURNING id
            """,
            (email_id, scheduled_date_str, status)
        )
        schedule_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return schedule_id

    def update_schedule(self, schedule_id, **fields):
        self._update('schedules', schedule_id, **fields)

    def get_schedule(self, schedule_id):
        self.cursor.execute("SELECT * FROM schedules WHERE id = %s", (schedule_id,))
        return self.cursor.fetchone()

    def delete_schedule(self, schedule_id):
        self.cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
        self.conn.commit()

    def get_all_schedules(self):
        self.cursor.execute("SELECT * FROM schedules")
        return self.cursor.fetchall()

    # User profile management
    def set_user_profile(self, **fields):
        self.cursor.execute("TRUNCATE TABLE user_profile")
        self.conn.commit()
        self.cursor.execute(
            """
            INSERT INTO user_profile (data) 
            VALUES (%s) 
            RETURNING id
            """,
            (json.dumps(fields),)
        )
        profile_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return profile_id

    def get_user_profile(self):
        self.cursor.execute("SELECT * FROM user_profile")
        profiles = self.cursor.fetchall()
        return profiles[0] if profiles else None

    def update_user_profile(self, **fields):
        existing_profile = self.get_user_profile()
        if existing_profile:
            self._update('user_profile', existing_profile[0], data=json.dumps(fields))
        else:
            self.set_user_profile(**fields)

    # Searching sent emails
    def search_sent_emails(self, keyword):
        self.cursor.execute(
            """
            SELECT * FROM sent_emails 
            WHERE 
                recipients ILIKE %s OR 
                subject ILIKE %s OR 
                body ILIKE %s
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        )
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Usage Example:
# db_manager = DatabaseManager(dbname="mydatabase", user="myuser", password="mypassword")
