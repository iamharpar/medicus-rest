from .views import AccountModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', AccountModelViewSet)

urlpatterns = router.urls
