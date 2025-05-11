# Mail Management System
<img src="https://cdn.intheloop.io/blog/wp-content/uploads/2019/03/loop-email-shared-inbox-feature.jpg">


## Overview
**Email Management App** is a comprehensive solution for scheduling, organizing, and managing emails. Built with Python and Streamlit, this application allows users to schedule emails to be sent at a later time, organize their inbox, and automate various email tasks to ensure efficient communication.

## Features
- Schedule emails to be sent at a later time
- Automatically organize your inbox
- Create custom email automation workflows
- Track email statuses (sent, pending, failed)
- User-friendly interface for easy management
- Secure and reliable email handling

## Installation
To get started with the Email Management App, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/sinanazem/mail-management-system.git
    ```

2. Navigate to the project directory:
    ```bash
    cd email-management-app
    ```

3. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file in the root directory and add your email configuration and other sensitive information:
    ```ini
    SMTP_HOST=YOUR_SMTP_HOST
    SMTP_PORT=587
    SMTP_USER=YOUR_EMAIL
    SMTP_PASS=YOUR_EMAIL_PASSWORD
    JWT_SECRET=YOUR_JWT_SECRET
    ```

6. Start the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Open the application in your web browser. By default, Streamlit runs on `localhost:8501`.
2. Sign up or log in to your account.
3. Use the dashboard to schedule and manage your emails.
4. Set up automation workflows to streamline your email tasks.

## Configuration
The application configuration is handled through environment variables stored in the `.env` file. Here are the key environment variables:

- **SMTP Configuration**:
    ```ini
    SMTP_HOST=YOUR_SMTP_HOST
    SMTP_PORT=587
    SMTP_USER=YOUR_EMAIL
    SMTP_PASS=YOUR_EMAIL_PASSWORD
    ```

- **App Settings**:
    ```ini
    JWT_SECRET=YOUR_JWT_SECRET
    ```



