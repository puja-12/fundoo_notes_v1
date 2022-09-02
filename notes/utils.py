import json
import logging
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from user.utils import Jwt
from notes.redis_cache import RedisFunction


def verify_token(function):
    """
    Token verification and authorization
    :param function:
    :return:
    """

    def wrapper(self, request):
        # print(dir(request))
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


class RedisNoteAPI:

    def get_note( self,user):
        data = RedisFunction.get_key(user)
        return json.loads(data) if data is not None else {}


    def create_note(self, user_id, note_id):
        data = self.get_note(user_id)
        data.update({note_id.get('id'): note_id})
        RedisFunction.set_key(user_id, json.dumps(data))

    def delete_note(self, user_id, note_id):
        note_dict = json.loads(RedisFunction.get_key(user_id))
        if note_dict.get(str(note_id)):
            note_dict.pop(str(note_id))
            RedisFunction.set_key(user_id, json.dumps(note_dict))

