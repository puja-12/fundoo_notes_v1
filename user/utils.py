from datetime import datetime, timedelta
from smtplib import SMTPAuthenticationError
from time import sleep

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from celery import shared_task

from user.token import Jwt


class Email:
    @staticmethod
    @shared_task
    def send_email(id, username, email):
        try:
            sleep(20)
            mail_subject = "Verification mail"
            token = Jwt.encode_token(payload={'user_id': id,
                                              'username': username

                                              })
            mail_message = "Click on this http://127.0.0.1:8000/user/verify/" + token

            send = send_mail(mail_subject,
                             mail_message,
                             settings.EMAIL_HOST_USER,
                             [email], fail_silently=False)


        except SMTPAuthenticationError as e:
            print(e)
            raise e

        except Exception as e:
            print(e)

    @classmethod
    def verify_user(cls, email, token):
        url = reverse("token_string", kwargs={"token": token})
        mail_subject = "Verification mail from celery"
        mail_message = f"Click on this {settings.BASE_URL}{url}"
        email_list = [email]
        cls.send_email(email_list, mail_subject, mail_message)