from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import shared_task
# @shared_task

smtp_server="smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = 'xfinite103@gmail.com'
SENDER_PASSWORD = 'cxvhbjaffmfbetrw'

def send_email_task(recp:str, subject:str, body:str):
    msg = MIMEMultipart()
    msg["To"] = recp
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(body))
    with SMTP(smtp_server,SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL,recp,msg.as_string())

def send_pdf_task(recp: str, subject: str, body: str, pdf_content: bytes, pdf_filename: str):
    msg = MIMEMultipart()
    msg["To"] = recp
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(body, 'plain'))
    pdf_attachment = MIMEApplication(pdf_content, _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
    msg.attach(pdf_attachment)
    try:
        with SMTP(smtp_server, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recp, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
