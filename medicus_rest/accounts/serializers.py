from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    medical_staff = MedicalStaffSerializer(required=False)
    organization = OrganizationSerializer(required=False)
    auth_token = serializers.SerializerMethodField('get_auth_token')

    class Meta:
        model = User
        fields = [
            'url', 'email', 'first_name', 'last_name', 'address',
            'medical_staff', 'user_type', 'auth_token', 'contact_detail',
            'organization',
        ]

    def get_auth_token(self, user):
        return user.get_auth_token()

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        if 'medical_staff' in validated_data:
            validated_data['medical_staff'] = MedicalStaff.objects.create(
                **validated_data['medical_staff']
            )
        else:
            validated_data['organization'] = Organization.objects.create(
                **validated_data['organization']
            )
        address = Address.objects.create(**address_data)
        user = User.objects.create(
            address=address, **validated_data
        )

        return user
