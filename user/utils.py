from datetime import datetime, timedelta
from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import send_mail

from user.token import Jwt


class Email:
    @staticmethod
    def verify_user(id, username, email):
        try:
            mail_subject = "Verification mail"
            token = Jwt.encode_token(payload={'user_id': id,
                                        'username': username

                                        })
            mail_message = "Click on this http://127.0.0.1:8000/user/verify/" + token

            send= send_mail(mail_subject,
                      mail_message,
                      settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)
            print(send,"fghjgh")


        except SMTPAuthenticationError as e:
            print(e)
            raise e

        except Exception as e:
            print(e)



