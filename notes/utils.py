import logging

from rest_framework import status
from rest_framework.response import Response

from user.models import User
from user.token import Jwt


def verify_token(function):
    """
    Token verification and authorization
    :param function:
    :return:
    """
    def wrapper(self, request):
        # print(dir(request))
        print(request.headers)
        if 'HTTP_TOKEN' not in request.META:
            response = Response({'message': 'Token not provided in the header'})
            response.status_code = 400
            logging.info('Token not provided in the header')
            return response

        token = request.META.get("HTTP_TOKEN")

        payload = Jwt.decode_token(token=token)
        print(payload)
        request.data.update({'user': payload.get('user_id')})

        return function(self, request)

    return wrapper
