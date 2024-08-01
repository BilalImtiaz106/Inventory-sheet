import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sheety_api_url = "https://api.sheety.co/36d99d20a77d9dff07026aea7c996682/schoolFee/user"
response = requests.get(url=sheety_api_url)
data = response.json()

print(data)

if 'user' in data:
    users = data['user']
else:
    raise KeyError("'user' key not found in the API response")

for record in users:
    name = record.get('name')  
    email = record.get('email') 
    paid = record.get('feesPaid') 
    if paid and paid.lower() != 'yes':
        print(f"{name} has not paid the fees.")

def send_email(from_email, password, to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

sender_email = input("Enter your email: ")
sender_password = input("Enter your email password: ")

for record in users:
    name = record.get('name') 
    email = record.get('email')  
    paid = record.get('feesPaid')  
    if paid and paid.lower() != 'yes':
        subject = "Reminder: School Fee Payment Due"
        body = f"Dear {name},\n\nOur records indicate that you have not yet paid the school fees. Please make the payment as soon as possible.\n\nThank you!"
        send_email(sender_email, sender_password, email, subject, body)
