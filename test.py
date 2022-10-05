from socket import *
from base64 import *
import ssl

recipient = input("Enter recipient email: ")
sender = input("Enter sender email: ")
password = input('Password: ')

msg = 'I love computer networks!'
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.office365.com"
port = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print ('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
	print ('250 reply not received from server.')

# Request an encrypted connection
startTlsCommand = 'STARTTLS\r\n'
clientSocket.send(startTlsCommand.encode())
tls_recv = clientSocket.recv(1024)

# Encrypt the socket
ssl_clientSocket = ssl.wrap_socket(clientSocket)

sender_address = b64encode(sender.encode())
password_address = b64encode(password.encode())

ssl_clientSocket.send(heloCommand.encode())

# Send the AUTH LOGIN command and print server response.
authCommand = 'AUTH LOGIN\r\n'
ssl_clientSocket.send(authCommand.encode())
auth_recv = ssl_clientSocket.recv(1024)
print(auth_recv)

#Send encrypted email address to server
ssl_clientSocket.send(sender_address +  '\r\n'.encode())
email_recv = ssl_clientSocket.recv(1024)
print(email_recv)

# Send password and print server response.
ssl_clientSocket.send(password_address + '\r\n'.encode())
pword_recv = ssl_clientSocket.recv(1024)
print(pword_recv)

# Send MAIL FROM command and print server response.
mailFromCommand = "MAIL FROM:"+ sender +"\r\n"
ssl_clientSocket.send(mailFromCommand.encode())
recv2 = ssl_clientSocket.recv(1024)
print(recv2)

# Send RCPT TO command and print server response.
rcptToCommand = "RCPT TO:" + recipient  +"\r\n"
ssl_clientSocket.send(rcptToCommand.encode())
recv3 = ssl_clientSocket.recv(1024)
print(recv3)

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
ssl_clientSocket.send(dataCommand.encode())
recv4 = ssl_clientSocket.recv(1024)
print(recv4)

# Send message data.
ssl_clientSocket.send(msg.encode())

# Message ends with a single period.
ssl_clientSocket.send(endmsg.encode())
recv5 = ssl_clientSocket.recv(1024)
print(recv5)

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
ssl_clientSocket.send(quitCommand.encode())
recv6 = ssl_clientSocket.recv(1024)
print(recv6)

ssl_clientSocket.close()
print('Mail sent successfully')