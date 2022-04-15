import smtplib, ssl


class EmailSender:
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "your-email-address"  # Enter your address
    receiver_email = "the-received0email-address"  # Enter receiver address
    p = "test_gmail_python"

    def __init__(self):
        pass

    @staticmethod
    def send(message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EmailSender.smtp_server, EmailSender.port, context=context) as server:
            server.login(EmailSender.sender_email, EmailSender.p)
            server.sendmail(EmailSender.sender_email, EmailSender.receiver_email, message)
