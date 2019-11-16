from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # All we need to specify in this view is a class variable that points to
    # the serializer-class which we want to use to create the object, i.e.
    # our `UserSerializer`
    # Thus, the RestFrameWork makes it really easy to create APIs that do
    # standard behaviour like creating objects in the data base.
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # sets the renderer, so we can view this endpoint in the browsable API
    renderer_classer = api_settings.DEFAULT_RENDERER_CLASSES
