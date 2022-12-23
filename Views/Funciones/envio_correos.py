from flask import Blueprint, Flask, render_template, request, json, session
from flask_mysqldb import MySQL
# from O365 import Message

# o365_auth = ('YourAccount@office365.com','YourPassword')
# m = Message(auth=o365_auth)
# m.setRecipients('reciving@office365.com')
# m.setSubject('I made an email script.')
# m.setBody('Talk to the computer, cause the human does not want to hear it any more.')
# m.sendMessage()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_content = "Hello, This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library"
#The mail addresses and password
sender_address = 'rosemberg.zambrano1177@correo.policia.gov.co'
sender_pass = 'Zaar2022++'
receiver_address = 'rosemberg.zambrano1177@correo.policia.gov.co'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'   
#The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')