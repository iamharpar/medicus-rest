from .models import Account
from rest_framework import serializers


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = [
            'url', 'email', 'first_name', 'last_name',
            'designation', 'organisation', 'is_employee'
        ]
