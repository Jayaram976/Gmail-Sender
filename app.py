from flask import Flask, render_template, request
import pandas as pd
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "jayaramkr1997@gmail.com"
EMAIL_PASSWORD = "egiw litl deao aomm"  # Use App Password

# Email template
EMAIL_TEMPLATES = {
    "interview_invite": """Subject: Interview Invitation from NovaTech Solutions

Dear {name},

Thank you for applying to the position of Junior Software Engineer at NovaTech Solutions. We are pleased to inform you that you have been shortlisted for the next round of our recruitment process.

We would like to schedule an interview with you to better understand your experience and skills.

Here are the proposed interview details:

🗓️ Date: April 8, 2025  
⏰ Time: 11:00 AM IST  
📍 Mode: Google Meet  
📌 Duration: 30–45 minutes  

Please confirm your availability by replying to this email by April 7, 2025, 5:00 PM IST.

We look forward to speaking with you!

Warm regards,  
Nikhil Arora  
HR Executive  
NovaTech Solutions  
hr@novatechsolutions.in  
+91-98400-XXXX"""
}

# Load contacts
def load_contacts():
    return pd.read_csv("contacts.csv")  # Assumes 'name' and 'email' columns

# Send email with PDF attachment
def send_email(to_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    # Body
    msg.attach(MIMEText(body, "plain"))

    # PDF Attachment
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    # Send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_template = request.form["style"]
        subject = "Interview Invitation from NovaTech Solutions"
        attachment = "Offer_Letter.pdf"  # PDF file in the root directory

        contacts = load_contacts()
        for _, row in contacts.iterrows():
            name = row["name"]
            email = row["email"]
            template = EMAIL_TEMPLATES[selected_template]
            message = template.replace("{name}", name)
            send_email(email, subject, message, attachment_path=attachment)

        return "✅ Interview emails with PDF sent successfully!"

    return render_template("index.html", styles=EMAIL_TEMPLATES.keys())

if __name__ == "__main__":
    app.run(debug=True)
