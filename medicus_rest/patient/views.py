from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
from accounts.permissions import IsOrganization, IsVerifiedMedicalStaff
# Create your views here.


class PatientModelViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsOrganization, IsVerifiedMedicalStaff]
