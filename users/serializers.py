from abc import ABC

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=50, required=True)
    password1 = serializers.CharField(min_length=5, max_length=20, write_only=True)
    password2 = serializers.CharField(min_length=5, max_length=20, write_only=True)

    def validate(self, data):
        print(data)
        email = data['email']
        username = data['username']
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is used.")

        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is used.")

        if data['password1'] != data['password2']:
            raise serializers.ValidationError("password1 and password2 must be equal.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        email = validated_data.pop("email")
        password = validated_data.pop("password1")

        return get_user_model().objects.create_user(
            email=email,
            password=password,
            **validated_data
        )


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer for the user object
    """

    token = serializers.CharField(source='auth_token', required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username', 'token', 'bio', 'image', ]
        extra_kwargs = {
            'password':
                {'write_only': True, 'min_length': 5},
            'token':
                {'read_only': True}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
            Update a user, setting the password correctly and return it
        """

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
        Serializer for the user authentication object
    """

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
