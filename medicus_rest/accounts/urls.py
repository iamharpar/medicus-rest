from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    UserModelViewSet, ping, UserLogin,
    UserLogout, check_user_logged_in,
)

router = DefaultRouter()
router.register(r'users', UserModelViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('ping/', ping, name='ping'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('check/', check_user_logged_in, name='check_login'),
]
