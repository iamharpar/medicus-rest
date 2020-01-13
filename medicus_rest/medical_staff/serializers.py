from rest_framework import serializers
from organization.models import Organization
from .models import MedicalStaff


class MedicalStaffSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = MedicalStaff
        fields = ['name', 'organization', 'role', 'speciality', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return dict(data)

    def create(self, validated_data):
        organization_name = validated_data.pop('organization', [])
        organization = Organization.objects.get(name=organization_name)
        validated_data.update({'organization': organization})
        return super().create(validated_data)