from rest_framework import viewsets
from rest_framework import status
from .serializers import UserSerializer
from .models import User


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            auth_token = response.data['auth_token']
            response.set_cookie('auth_token', auth_token)
        return response
