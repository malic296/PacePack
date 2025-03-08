import random
from smtplib import SMTPException
from flask_mail import Mail, Message

mail = Mail()

def send_verification_code(email, verification_code):
    msg = Message("Email Verification", recipients=[email])
    msg.body = f"Your verification code is: {verification_code}"
    try:
        with mail.connect() as conn:
            conn.send(msg)
        return True
    except SMTPException as e:
        print(f"Error sending email: {e}")
        return False

def generate_verification_code():
    code = str(random.randint(100000, 999999))
    return code