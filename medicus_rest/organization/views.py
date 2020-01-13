from rest_framework import generics
from accounts.serializers import OrganizationSerializer
from .models import Organization
# Create your views here.


class OrganizationModeAPIView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
