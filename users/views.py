from rest_framework import generics, authentication, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from .models import FollowingUsers
from .serializers import UserSerializer, \
    AuthTokenSerializer, \
    UserRegistrationSerializer, \
    UserProfileSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True)


class UserProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class FollowUsersView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        user = request.user
        other_user = get_user_model().objects.filter(username=username)[0]

        if FollowingUsers.objects.is_following(user, other_user):
            raise ValidationError("You already follow the user.")

        FollowingUsers.objects.follow(user, other_user)

        return Response({'message': f'Following User {other_user.username} done.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        print(username)
        user = request.user
        other_user = get_user_model().objects.filter(username=username)[0]
        print(other_user)

        if not FollowingUsers.objects.is_following(user, other_user):
            raise ValidationError("You don't follow the user.")

        FollowingUsers.objects.unfollow(user, other_user)

        return Response({'message': f'Unfollowing user {other_user.username} done.'}, status=status.HTTP_204_NO_CONTENT)
