import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class Jwt:
    @staticmethod
    def encode(payload):

        return jwt.encode(payload, settings.JWT_SECRET_KEY, "HS256")

    @staticmethod
    def decode(token):
        return jwt.decode(token, settings.JWT_SECRET_KEY, ["HS256"])
