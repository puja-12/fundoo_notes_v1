import logging
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from user.models import User
from user.serializers import RegisterSerializer
from user.token import Jwt
from user.utils import Email

logger = logging.getLogger('django')


class UserRegisterApiView(APIView):

    def post(self, request):
        """
        post method for registering a user
        """
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Email.verify_user(id=serializer.data.get('id'), username=serializer.data.get('username'),
                              email=serializer.data.get('email'))

            return Response(
                {"message": "Registration Successful, Please verified your Email ", "data": serializer.data},
                status.HTTP_200_OK)

        except ValidationError as e:
            logger.exception(e)
            return Response({'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(e)
            return Response({'message': 'invalid details'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(APIView):

    def post(self, request):
        """
         post method for checking login operation
        """

        try:

            user = authenticate(username=request.data.get("username"),password=request.data.get("password"))
            if user and user.is_verify:

                logger.info("User is successfully logged in")
                return Response({'success': True, 'message': 'Login Success', 'data': {'token_key': user.token}}
                                ,status=status.HTTP_200_OK)

            return Response({'success': False, 'message': 'Invalid credentials used!'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class VarifyUser(APIView):
    """
    Validating the token if the user is valid or not
    """

    def get(self, request, token):
        try:
            decode_token = Jwt.decode_token(token=token)
            user = User.objects.get(username=decode_token.get('username'))
            user.is_verify = True
            user.save()
            return Response({"message": "Validation Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

