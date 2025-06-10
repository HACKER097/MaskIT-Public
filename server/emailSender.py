import smtplib
from email.mime.text import MIMEText
CLIENT_ID = ''
CLIENT_SECRET = ''
subject = "Verify Your Account on MaskIT"
sender = "mask.IT.MIT@gmail.com"
password = 'phaomtebwmobngab'
def send_email(recipients,name,link):
    try:
        body = f"Dear {name},\n\nThank you for using MaskIT. We're excited to have you on board!\nTo ensure the utmost protection for your account, we kindly ask you to complete the verification process.\n\nPlease click on the following link to verify your account:\n\n{link}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        return True
    except:
        return False
