import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt

def send_email(to_email, subject, body):
    sender_email = "bookrecommenderai@gmail.com"
    sender_password = "ginetdlbneuprvbw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print(f"DEBUG: Sending Email to {to_email} with subject '{subject}'")  # ✅ Debugging
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email Sent Successfully to {to_email}")  # ✅ Confirm email is sent
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def send_otp_email(to_email, otp, purpose):
    subject_map = {
        'signin': "Your OTP to sign in",
        'signup': "Your OTP for account creation",
        'reset': "Your OTP to reset your password"
    }
    subject = subject_map.get(purpose, "Your OTP")
    body = f"Your OTP is {otp}. This OTP is valid for 10 minutes."

    print(f"DEBUG: Sending OTP Email - To: {to_email}, OTP: {otp}, Purpose: {purpose}")  # ✅ Log the email sending

    email_sent = send_email(to_email, subject, body)

    if not email_sent:
        print(f"❌ ERROR: Failed to send OTP to {to_email}")  # ✅ Log failures
    else:
        print(f"✅ SUCCESS: OTP email sent to {to_email}")  # ✅ Confirm success

    return email_sent


    
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

import bcrypt

def encrypt_security_answer(answer):
    return bcrypt.hashpw(answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_security_answer(answer, hashed_answer):
    if not answer.strip():  # Prevent blank answers from being accepted
        return False
    return bcrypt.checkpw(answer.encode('utf-8'), hashed_answer.encode('utf-8'))

def send_otp_signin(to_email, otp):
    sender_email = "bookrecommenderai@gmail.com"
    sender_password = "ginetdlbneuprvbw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Your OTP to signin into Application"

    body = f"Your OTP is {otp}. This OTP is valid for 10 minutes."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

def send_otp_reset(to_email, otp):
    sender_email = "bookrecommenderai@gmail.com"
    sender_password = "ginetdlbneuprvbw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Your OTP to reset the password"

    body = f"Your OTP is {otp}. This OTP is valid for 10 minutes."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

def send_otp_signup(to_email, otp):
    sender_email = "bookrecommenderai@gmail.com"
    sender_password = "ginetdlbneuprvbw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Your OTP for creating the new user in application"

    body = f"Your OTP is {otp}. This OTP is valid for 10 minutes."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()