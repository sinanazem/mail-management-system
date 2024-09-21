from datetime import datetime, timedelta
import time
import os
import threading
from loguru import logger
from src.utils.database import DatabaseManager
from src.email_scheduler import send_email


db = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )


def check_and_send_emails():
    """Check the database for future emails and send them if it's time."""
    future_emails = db.get_all_schedules()
    
    if not future_emails:
        logger.info("No emails to schedule.")
        return None
    
    now = datetime.now().replace(second=0, microsecond=0)  # Strip seconds and microseconds
    closest_email_time = None
    
    for s_email in future_emails:
        
        # Check if it's time to send the email (ignoring seconds) and the email is pending or failed
        if s_email[2] <= now and s_email[3] in ['Pending', 'Failed']:
            try:
                email = db.get_sent_email(s_email[1])
                logger.info(f"Sending email to {email[1]}")
                send_email(email[1], email[2], email[3])
                
                # Update status to 'sent' after successful send
                db.update_schedule(s_email[0], status="Sent")
                logger.info(f"Email sent to {email[1]} and status updated to 'sent'")
            except Exception as e:
                # Log the error and update status to 'failed'
                logger.error(f"Failed to send email to {email[1]}. Error: {str(e)}")
                db.update_schedule(s_email[0], status="Failed")
                logger.info(f"Email status updated to 'failed' for {email[1]}")
    
    return closest_email_time



def schedule_dynamic_check():
    """Dynamically schedule checks based on the next email time."""
    while True:
        closest_email_time = check_and_send_emails()
        if closest_email_time:
            now = datetime.now().replace(second=0, microsecond=0)
            sleep_duration = (closest_email_time - now).total_seconds()
            
            # Ensure we don't sleep for a negative or too small interval
            if sleep_duration > 0:
                logger.info(f"Waiting {sleep_duration:.2f} seconds until next email at {closest_email_time}")
                time.sleep(sleep_duration)
            else:
                logger.info(f"Scheduled time {closest_email_time} is in the past, checking again immediately.")
        else:
            logger.info("No future emails found. Checking again in 10 seconds.")
            time.sleep(10)  # Check again after 10 seconds if no future emails


if __name__ == '__main__':
    # Start the dynamic email scheduler
    logger.info("Starting the dynamic email scheduler...")
    schedule_dynamic_check()