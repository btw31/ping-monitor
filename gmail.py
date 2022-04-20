import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(subject, body):
    gmail_user = 'email'
    gmail_password = 'pwd'
    
    #body = "Hello, \nThis is a test email\nBrent"
    sender = gmail_user
    receiver = "email"
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver 
    message['Subject'] = subject
    message.attach(MIMEText(body, "plain"))
    session = smtplib.SMTP_SSL("smtp.gmail.com")
    session.login(gmail_user, gmail_password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
