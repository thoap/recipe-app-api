from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
# AND
# https://www.django-rest-framework.org/api-guide/generic-views/#createapiview


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # set extra restrictions or arguments for the fields that will be
        # referenced in `fields` with the help of `extra_kwargs`
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it

        We modify this function in a way, that our model manager create
        function is called (`app.core.models.UserManager.create_user`),
        instead of the default `create`.

        When we're ready to create the user the RestFrameWork will call
        this function and pass in the `validated_data`. The `validated_data`
        will contain all of the data which was passed into the serializer, i.e.
        the JSON-data coming from an http-post. That data is used to create the
        user.
        """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentification object. This is going
    to be used to authenticate requests."""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user. We here retrieve the password
        from the passed in `attrs` (attrbutes) and validate it.
        We adapt this function so it accepts the user email instead of the
        default user name (see the `authenticate` function further below."""

        email = attrs.get('email')
        password = attrs.get('password')

        # username will be set to email, b/c `username` is the parameter used
        # by the function `authenticate` and we are authenticating via email
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            # Django RestFramework knows how to handle this error by passing
            # the error as a 400 response and sending that to the user plus
            # attaching the message `msg`
            raise serializers.ValidationError(msg, code='authentification')

        attrs['user'] = user

        # whenever adapting `validate` you must return the attributes at the
        # end
        return attrs
