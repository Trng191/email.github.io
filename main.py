import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import decode_header
import screenshot
import shutdown

username_sender = "test.sender.pp@gmail.com"
password_sender = "mqre gihn qzct yulz"
username_receiver = "mangmaytinhremotecontrol@gmail.com"
password_receiver = "lmlx vrwx cwym hvqz"

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS


def send_email(sender, receiver, subject, body, isSender, image_data=None):
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
    if (isSender == True):
        server.login(username_sender, password_sender)
    else:
        server.login(username_receiver, password_receiver)
    server.sendmail(sender, receiver, text)
    server.quit()


def fetch_and_process_emails():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username_receiver, password_receiver)
    status, messages = imap.select("INBOX")
    N = 1
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                subject = subject.lower()
                if subject == "screenshot":
                    image_data = screenshot.screen_shot()
                    send_email(username_receiver, username_sender, "Screenshot taken",
                               "See attachment: ", False, image_data)
                elif subject == "shutdown":
                    shutdown.shutdown()
                else:
                    send_email(username_receiver, username_sender,
                               "Invalid command", "Command not found", False)
    imap.close()
    imap.logout()


while True:
    subject = input("Enter subject: ")
    body = input("Enter body: ")
    send_email(username_sender, username_receiver, subject, body, True)
    fetch_and_process_emails()
    command = input("Enter E to exit, enter any other key to continue: ")
    if (command == "E" or command == "e"):
        break
