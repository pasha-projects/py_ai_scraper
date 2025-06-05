import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os

from web_summarizer import summarize_url  # must return a nicely formatted string

def send_email(summary, recipient_email):
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not password:
        raise ValueError("Missing SENDER_EMAIL or GMAIL_APP_PASSWORD in .env")

    msg = EmailMessage()
    msg.set_content(summary)
    msg["Subject"] = "Web Summary"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Gmail SMTP
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

def main():
    url = input("Enter the URL to summarize: ").strip()
    summary = summarize_url(url)
    print("\n--- Summary ---\n", summary)

    recipient_email = input("\nEnter your email address to send the summary: ").strip()
    send_email(summary, recipient_email)
    print("✅ Email sent successfully.")

if __name__ == "__main__":
    main()
