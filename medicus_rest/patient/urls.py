from rest_framework.routers import DefaultRouter
from .views import PatientModelViewSet

router = DefaultRouter()
router.register(r'', PatientModelViewSet)

urlpatterns = router.urls
