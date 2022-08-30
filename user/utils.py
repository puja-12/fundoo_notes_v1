from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import send_mail

from user.token import Jwt


class Email:
    @staticmethod
    def verify_user(id, username, email):
        try:
            mail_subject = "Verification mail"
            token = Jwt.encode(payload={'user_id': id,
                                        'username': username,
                                        })
            mail_message = f"Click on this http://127.0.0.1:8000/user/verify/{token}"
            print(mail_message)
            send_mail(mail_subject,
                      mail_message,
                      settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)


        except SMTPAuthenticationError as e:
            print(e)
            raise e

