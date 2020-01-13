from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'description', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return dict(data)
