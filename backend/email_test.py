import smtplib


def send_email(recipient_email, subject, body):
    # Configure your email server and sender email here
    sender_email = "barkandbones.orders@gmail.com"
    password = "ogwp vpet areb uuou"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

send_email("dannyhudetz@gmail.com", "AHHH", "BBAHHHH")