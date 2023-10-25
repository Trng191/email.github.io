import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import decode_header
import screenshot
import shutdown

username = "mangmaytinhremotecontrol@gmail.com"
password = "lmlx vrwx cwym hvqz"

imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
imap_server.login(username, password)
imap_server.select("inbox")

function_map = {
    "screenshot": screenshot.screen_shot,
    "shutdown": shutdown.shutdown,
    # Add more commands and corresponding functions as needed
}

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
    server.login(username, password)
    server.sendmail(sender, receiver, text)
    server.quit()


def fetch_and_process_emails():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
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
                    send_email(username, username, "Screenshot taken",
                               "See attachment: ", image_data)
                elif subject == "shutdown":
                    shutdown.shutdown()
                else:
                    send_email(username, username,
                               "Invalid command", "Command not found")
    imap.close()
    imap.logout()


while True:
    subject = input("Enter subject: ")
    body = input("Enter body: ")
    send_email(username, username, subject, body)
    fetch_and_process_emails()
    command = input("Enter E to exit, enter any other key to continue: ")
    if (command == "E" or command == "e"):
        break


imap_server.logout()
