# email_sender_system/main.py

from flask import Flask, request, render_template, redirect
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

COMMON_DOMAINS = [".com", ".co.in", ".net", ".org", ".in", ".inc", ".corp", ".tech", ".global", ".io", ".solutions", ".group", ".company", ".biz"]
EMAIL_PATTERNS = [
    "{first}.{last}",
    "{first[0]}.{last}",
    "{first}.{last[0]}",
    "{first}{last}",
    "{first}",
    "{first[0]}{last}",
    "{first[0]}.{last[0]}",
    "{first}_{last}",
    "{last}.{first}"
]

def generate_emails(full_name, org_name):
    parts = full_name.strip().lower().split()
    if len(parts) != 2:
        return []
    first, last = parts
    org = org_name.strip().lower().replace(" ", "")
    emails = set()
    for pattern in EMAIL_PATTERNS:
        local_part = pattern.format(first=first, last=last, first0=first[0], last0=last[0])
        for domain in COMMON_DOMAINS:
            emails.add(f"{local_part}@{org}{domain}")
    return list(emails)

def send_email(subject, body, from_email, password, to_emails, attachment=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = from_email
    msg["Bcc"] = ", ".join(to_emails)
    msg.set_content(body)

    if attachment:
        filename = attachment.filename
        file_data = attachment.read()
        file_type = attachment.mimetype
        maintype, subtype = file_type.split('/', 1)
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        full_name = request.form["full_name"]
        org_name = request.form["org_name"]
        subject = request.form["subject"]
        body = request.form["body"]
        from_email = request.form["from_email"]
        password = request.form["password"]
        attachment = request.files.get("attachment")

        to_emails = generate_emails(full_name, org_name)
        send_email(subject, body, from_email, password, to_emails, attachment)
        return f"<h3>Email sent to: {', '.join(to_emails)}</h3>"

    return render_template("form.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

