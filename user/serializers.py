from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone', 'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


