import imaplib
import email

server = 'imap.gmail.com'
account = 'test.sender.pp@gmail.com'
password = 'mqre gihn qzct yulz'

imap = imaplib.IMAP4_SSL(host = server, port = 993)
    
imap.login(account, password)

_, count = imap.select("Inbox")

print(count[0].decode())

imap.close()

imap.logout()