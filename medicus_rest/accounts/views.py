from rest_framework import viewsets

from .serializers import AccountSerializer
from .models import Account


class AccountModelViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
