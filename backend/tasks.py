from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import shared_task
# @shared_task

def send_email_task(recp:str, subject:str, body:str):
    smtp_server="smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = 'xfinite103@gmail.com'
    SENDER_PASSWORD = 'cxvhbjaffmfbetrw'
    msg = MIMEMultipart()
    msg["To"] = recp
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(body))
    with SMTP(smtp_server,SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL,recp,msg.as_string())



