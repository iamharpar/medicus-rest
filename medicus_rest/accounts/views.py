from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import viewsets
from rest_framework import status
from .serializers import UserSerializer
from .models import User

# Okay ! So hear me out on this one. After a discussion about this, with champa
# "we" concluded that the entire workflow of this application will be based
# on REST ful services, but since the guidelines for developing a RESTfull
# service are a bit shaky, we will be utilizing both tokens as well as a
# cookie based workflow. During Sign up and Login process the backend will be
# responsible for setting and deleting cookies with the respective `auth_token`
# on the client side. The same `auth_tokens` will also be sent with the
# response body in JSON format.
#
# Although doing so will break the consistency of this RESTful service since,
# now this service cannot be consumed by any application which does not
# implement a cookie interface. So we will work on an assumption that this,
# API will only be consumed by a web based application rendering the entire
# RESTfull service kinda useless.
# Man ! that's depressing. :-(


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            auth_token = response.data['auth_token']
            response.set_cookie(key='auth_token', value=auth_token)
        return response


class UserLogin(TokenCreateView):

    def post(self, request, **kwargs):
        response = super().post(request, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            auth_token = response.data['auth_token']
            response.set_cookie(key='auth_token', value=auth_token)
        return response


class UserLogout(TokenDestroyView):

    def post(self, request, **kwargs):
        response = super().post(request, **kwargs)
        # This is expected behaviour
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response.delete_cookie(key='auth_token')
        return response
