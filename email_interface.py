import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username_sender = "test.sender.pp@gmail.com"
password_sender = "mqre gihn qzct yulz"

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS


def send_email(sender, receiver, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        text = msg.as_string()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username_sender, password_sender)
        server.sendmail(sender, receiver, text)
    except Exception as e:
        print(e)
    finally:
        server.quit()
