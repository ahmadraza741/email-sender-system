from flask import Flask, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os

app = Flask(__name__)

# Email credentials (set these in environment variables or replace directly)
FROM_EMAIL = os.getenv("EMAIL") or "your_email@gmail.com"
EMAIL_PASSWORD = os.getenv("PASSWORD") or "your_password"

# Common domain patterns
COMMON_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "company.com", "organization.org"
]

def generate_emails(name, org):
    name = name.lower().replace(" ", "")
    org = org.lower().replace(" ", "")
    local_parts = [name, f"{name}.{org}", f"{org}.{name}", f"{name}_{org}"]
    domains = [org + ".com", org + ".org"] + COMMON_DOMAINS
    return [f"{lp}@{domain}" for lp in local_parts for domain in domains]

def send_email(subject, body, from_email, password, to_emails, attachment=None):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # ✅ Add attachment if it exists
    if attachment:
        part = MIMEApplication(attachment.read(), Name=attachment.filename)
        part['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, password)
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        org = request.form["organization"]
        attachment = request.files.get("attachment")

        subject = f"Hello from {name}"
        body = f"Hi, I'm {name} from {org}. Let's connect!"

        recipients = generate_emails(name, org)

        send_email(subject, body, FROM_EMAIL, EMAIL_PASSWORD, recipients, attachment)

        return f"✅ Email sent successfully to:<br><br>" + "<br>".join(recipients)

    return render_template("form.html")
