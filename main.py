# email_sender_system/main.py

from flask import Flask, request, render_template, redirect
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

COMMON_DOMAINS = [".com", ".co.in", ".net", ".org", ".in"]
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

def send_email(subject, body, from_email, password, to_emails):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg.set_content(body)

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

        to_emails = generate_emails(full_name, org_name)
        send_email(subject, body, from_email, password, to_emails)
        return f"<h3>Email sent to: {', '.join(to_emails)}</h3>"

    return render_template("form.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# templates/form.html
# Save this under a folder named 'templates' in your project

# Contents of form.html:
#
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Smart Email Sender</title>
#     <style>
#         body { font-family: Arial; margin: 40px; }
#         label { display: block; margin-top: 10px; }
#         input, textarea { width: 100%; padding: 8px; margin-top: 4px; }
#         button { margin-top: 15px; padding: 10px 20px; }
#     </style>
# </head>
# <body>
#     <h2>Send Email by Name & Organization</h2>
#     <form method="POST">
#         <label>Full Name:</label>
#         <input type="text" name="full_name" required />
#         <label>Organization Name:</label>
#         <input type="text" name="org_name" required />
#         <label>Email Subject:</label>
#         <input type="text" name="subject" required />
#         <label>Email Body:</label>
#         <textarea name="body" rows="6" required></textarea>
#         <label>Your Email (Gmail):</label>
#         <input type="email" name="from_email" required />
#         <label>Your Email Password (App Password):</label>
#         <input type="password" name="password" required />
#         <button type="submit">Send Email</button>
#     </form>
# </body>
# </html>
