from abc import ABC

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone', 'location', 'id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    # password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    model = User

    # def validate_new_password(self, value):
    #     validate_password(value)
    #     return value
