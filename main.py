import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from passwords import EMAIL_ADDRESS, PASSWORD
import yaml


def send_email():
    with open('mail_info\\config.yml', 'r') as config_file:
        config_data = yaml.safe_load(config_file)
        recipients = config_data['recipients']
        subject = config_data['subject']

    with open('mail_info\\message.txt', 'r', encoding='utf-8') as message_file:
        message_text = message_file.read()

    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    message.attach(MIMEText(message_text, 'plain'))

    attachments = config_data.get('attachments', [])
    for attachment in attachments:
        with open(attachment, 'rb') as file:
            part = MIMEApplication(file.read())
            part.add_header('Content-Disposition', 'attachment', filename=attachment)
            message.attach(part)

    smtp_server = 'smtp.yandex.ru'
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        server.send_message(message)

    print('Письмо успешно отправлено!')


send_email()
