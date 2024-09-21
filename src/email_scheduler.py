import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Email configuration
sender_email = os.getenv(key='sender_email')
sender_password = os.getenv(key='sender_password')
    


def send_email(to_email, subject, body):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))
    
    # Try to connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        logger.info("Email sent successfully!")
        return "Sent"
    except Exception as e:
        logger.info(f"Failed to send email: {e}")
        return f"Failed: {e}"