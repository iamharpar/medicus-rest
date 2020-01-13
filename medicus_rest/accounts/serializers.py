from rest_framework import serializers
from organization.models import Organization
from organization.serializers import OrganizationSerializer
from medical_staff.models import MedicalStaff
from medical_staff.serializers import MedicalStaffSerializer

from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return dict(data)


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    medical_staff = MedicalStaffSerializer(required=False)
    organization = OrganizationSerializer(required=False)
    auth_token = serializers.SerializerMethodField('get_auth_token')

    class Meta:
        model = User
        fields = [
            'url', 'email', 'address', 'medical_staff', 'user_type',
            'auth_token', 'contact_detail', 'organization',
        ]
        extra_kwargs = {
            'contact_detail': {'required': True},
            'user_type':  {'required': True},
        }

    def get_auth_token(self, user):
        return user.get_auth_token()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return dict(data)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        if 'medical_staff' in validated_data:
            validated_data['medical_staff'] = MedicalStaff.objects.create(
                **validated_data['medical_staff']
            )
        if 'organization' in validated_data:
            validated_data['organization'] = Organization.objects.create(
                **validated_data['organization']
            )
        address = Address.objects.create(**address_data)
        user = User.objects.create(
            address=address, **validated_data
        )

        return user
