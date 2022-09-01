import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class Jwt:
    @staticmethod
    def encode_token(payload):
        """
        Encoding
        :return:
        """
        try:
            if payload.get('exp') is None:
                payload.update({"exp": settings.JWT_EXPIRING_TIME})

            return jwt.encode(payload, settings.JWT_SECRET_KEY,
                                       algorithm="HS256")
            return token_encoded
        except Exception as e:
            logging.exception(e)
            return Response({'Message': 'Unexpected error'}, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def decode_token(token):
        """
        Decoding
        :return:
        """
        return  jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])


