from django.urls import path
from .views import (
    OrganizationModeAPIView
)

urlpatterns = [
    path('', OrganizationModeAPIView.as_view(), name='organization'),
]
