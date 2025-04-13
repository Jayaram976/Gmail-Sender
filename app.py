from flask import Flask, render_template, request
import pandas as pd
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "jayaramkr1997@gmail.com"
EMAIL_PASSWORD = "egiw litl deao aomm"  # Use App Password

# Email sender function
def send_email(to_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form["subject"]
        message_template = request.form["message"]
        file = request.files["csv_file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            name = row["name"]
            email = row["email"]
            message = message_template.replace("{name}", name)
            send_email(email, subject, message, attachment_path="Offer_Letter.pdf")

        return "✅ Emails sent successfully!"

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
