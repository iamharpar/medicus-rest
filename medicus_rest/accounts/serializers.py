from rest_framework import serializers
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField('get_auth_token')
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            'url', 'email', 'first_name', 'last_name', 'address',
            'user_type', 'auth_token', 'contact_detail',
        ]

    def get_auth_token(self, user):
        return user.get_auth_token()

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        user = User.objects.create(address=address, **validated_data)
        return user
