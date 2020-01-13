from rest_framework import serializers
from organization.serializers import OrganizationSerializer
from medical_staff.serializers import MedicalStaffSerializer
from django.utils.translation import ugettext_lazy as _

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

    def get_user_type_serializer_instance(self, validated_data):
        is_medical_staff = 'medical_staff' in validated_data
        is_organization = 'organization' in validated_data

        if is_medical_staff and is_organization:
            raise serializers.ValidationError(_(
                "`user` cannot be both, kindly give data for "
                "request body should respect the `user_type` field"
            ))

        if not (is_medical_staff or is_organization):
            raise serializers.ValidationError(_(
                "no `user_type` related details provided"
            ))

        if is_medical_staff:
            self.user_type = 'medical_staff'
            return MedicalStaffSerializer(data=validated_data[self.user_type])

        if is_organization:
            self.user_type = 'organization'
            return OrganizationSerializer(data=validated_data[self.user_type])

    def create_address(self, validated_data):
        address_data = validated_data['address']
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address_instance = address_serializer.save()
        validated_data.update({'address': address_instance})
        return validated_data

    def create_user_type_instance(self, validated_data):
        user_type_serializer = self.get_user_type_serializer_instance(
            validated_data
        )
        user_type_serializer.is_valid(raise_exception=True)
        user_type_instance = user_type_serializer.save()
        validated_data.update({self.user_type: user_type_instance})
        return validated_data

    def create(self, validated_data):
        validated_data = self.create_user_type_instance(validated_data)
        validated_data = self.create_address(validated_data)
        return User.objects.create(**validated_data)
