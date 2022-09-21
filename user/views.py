import logging
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from user.models import User
from user.serializers import RegisterSerializer, ChangePasswordSerializer
from user.token import Jwt
from user.utils import Email
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger('django')


class UserRegisterApiView(APIView):
    @swagger_auto_schema(
        operation_summary="registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='location'),
            }
        ))
    def post(self, request):
        """
        post method for registering a user
        """
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            Email.send_email(id=serializer.data.get('id'), username=serializer.data.get('username'),
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
    @swagger_auto_schema(
        operation_summary="login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            }
        ))
    def post(self, request):
        """
         post method for checking login operation
        """

        try:

            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user and user.is_verify:
                logger.info("User is successfully logged in")

                return Response({'success': True, 'message': 'Login Success', 'data': {'token_key': user.token}})

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


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.data

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user= User.objects.get(username=request.data.get("username"),)

            # password = serializer.data.get("password")
            # if not user.check_password(password):
            #     return Response({"password": ["Wrong password."]},
            #                     status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "updated Successfully"},status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from  django.utils.deprecation import MiddlewareMixin