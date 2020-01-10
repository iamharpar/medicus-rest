from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField('get_auth_token')

    class Meta:
        model = User
        fields = [
            'url', 'email', 'first_name', 'last_name', 'address',
            'is_organisation', 'is_medical_staff', 'auth_token',
            'contact_detail',
        ]

    def get_auth_token(self, user):
        return user.get_auth_token()
