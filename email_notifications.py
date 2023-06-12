import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta

# Set cooldown period (in seconds) for each notification
cooldown_period = 300  # 5 minutes

# Dictionary to store cooldown timestamps for each notification
cooldowns = {}

def send_email(subject, message):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if subject in cooldowns and datetime.now() - cooldowns[subject] < timedelta(seconds=cooldown_period):
        # Notification is still in cooldown period, skip sending email
        print(f"Skipping email for {subject}: cooldown period active")
        return

    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject=subject,
        plain_text_content=message)

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent - Subject: {subject}")
        cooldowns[subject] = datetime.now()  # Update cooldown timestamp
    except Exception as e:
        print(f"Email sending failed - Subject: {subject}")
        print(str(e))