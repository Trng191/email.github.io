import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "test.sender.pp@gmail.com"
receiver_email = "ptbtin22@clc.fitus.edu.vn"
password = "mqre gihn qzct yulz"
#mqre gihn qzct yulz

subject = input("Enter your subject here: ")
message = input("Enter your message here: ")

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(message, "plain"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()  # Use TLS for security
server.login(sender_email, password)  # Login to your email account

# Send the email
server.sendmail(sender_email, receiver_email, msg.as_string())

# Quit the server
server.quit()