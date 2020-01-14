from rest_framework import serializers
from organization.models import Organization
from django.utils.translation import ugettext_lazy as _
from .models import MedicalStaff


class MedicalStaffSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = MedicalStaff
        organization = serializers.CharField()
        fields = ['name', 'organization', 'role', 'speciality', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return dict(data)

    def get_organization(self, organization_name):
        organization = Organization.objects.filter(
            name=organization_name
        ).first()

        if organization is None:
            raise serializers.ValidationError(_(
                "Organization with name {} does not exists !".format(
                    organization_name
                )
            ))

        return organization

    def create(self, validated_data):
        organization_name = validated_data.pop('organization', [])
        organization = self.get_organization(organization_name)
        validated_data.update({'organization': organization})
        return super().create(validated_data)
