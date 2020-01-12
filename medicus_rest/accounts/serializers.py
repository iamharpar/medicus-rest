from rest_framework import serializers
from .models import (
    User, Address, MedicalStaff, Organization
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['description', ]


class MedicalStaffSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = MedicalStaff
        fields = ['organization', 'role', 'speciality', ]

    def create(self, validated_data):
        organization_name = validated_data.pop('organization', [])
        organization = Organization.objects.get(name=organization_name)
        validated_data.update({'organization': organization})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        organization_name = validated_data.pop('organization', [])
        organization = Organization.objects.get(name=organization_name)
        instance.organization = organization
        instance.save()
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user_extra = serializers.SerializerMethodField('get_extra_user_data')
    auth_token = serializers.SerializerMethodField('get_auth_token')

    class Meta:
        model = User
        fields = [
            'url', 'email', 'first_name', 'last_name', 'address',
            'user_type', 'auth_token', 'contact_detail', 'user_extra',
        ]

    def get_auth_token(self, user):
        return user.get_auth_token()

    def get_extra_user_data(self, user):
        self.extra_initial_data = self.initial_data['extra']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        user = User.objects.create(address=address, **validated_data)
        return user
