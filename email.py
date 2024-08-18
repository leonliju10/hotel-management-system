import random
import smtplib
from email.message import EmailMessage
otp= " "
for i in range(6):
        otp+= str (random.randint(0,9))

print(otp)
server = smtplib.SMTP('smtp-gmail.com', 587)
server.starttls()
server.login('sprashantofficial@gmail.com', 'iufu kppl tvgd yakj')
to_mail = input("Enter your email: ")
msg = EmailMessage()
msg[ 'Subject'] = "OTP Verification"
msg[ 'From' ] =from_mail
msg['To'] = to_mail
msg. set_content ("Your OTP is: " +otp)
server .send_message(msg)
input_otp = input("Enter OTP: ")
if input_otp == otp:
    print("oTP Verified")
else:
    print("Invalid oTp")
print("Email sent")