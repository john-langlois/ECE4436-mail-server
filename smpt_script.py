import smtplib

SENDER = input('sender:')
LOGIN    = SENDER
PASSWORD = input("password:")
RECEIVER  = [input("recipient: ")]
SUBJECT  = "ECE4436 Lab 1"

msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (SENDER, ", ".join(RECEIVER), SUBJECT) )
msg += "smtplib script is working\r\n"

server = smtplib.SMTP('smtp.office365.com', 587)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(LOGIN, PASSWORD)
server.sendmail(SENDER, RECEIVER, msg)
server.quit()