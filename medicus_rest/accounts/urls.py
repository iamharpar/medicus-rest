from django.urls import path, include
from .serializers import AccountViewSerializer
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'', AccountViewSerializer)
urlpatterns = [
    path(r'', include(router.urls)),
]