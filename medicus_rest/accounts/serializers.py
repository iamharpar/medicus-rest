from rest_framework import serializers
from .models import (
    User, Address
)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    extra = serializers.SerializerMethodField('create_required_user_type')
    auth_token = serializers.SerializerMethodField('get_auth_token')

    class Meta:
        model = User
        fields = [
            'url', 'email', 'first_name', 'last_name', 'address',
            'user_type', 'auth_token', 'contact_detail', 'extra',
        ]

    def get_auth_token(self, user):
        return user.get_auth_token()

    def create_required_user_type(self, user):
        print(user)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        user = User.objects.create(address=address, **validated_data)
        return user
