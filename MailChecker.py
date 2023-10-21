import imaplib
import email

server = 'imap.gmail.com'
account = 'mangmaytinhremotecontrol@gmail.com'
password = 'lmlx vrwx cwym hvqz'

imap = imaplib.IMAP4_SSL(host = server, port = 993)
    
imap.login(account, password)

_, count = imap.select("Inbox")

print(count[0].decode())

imap.close()

imap.logout()
