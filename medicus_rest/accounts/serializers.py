from .models import Account
from rest_framework import serializers, viewsets

class AcountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'email', 'first_name', 'last_name', 'designation', 'is_employee']
    

class AccountViewSerializer(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AcountSerializer