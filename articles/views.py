from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response

from core.utils import generate_random_string
from users.models import FollowingUsers
from .filters import ArticleFilter
from .models import Article
from .serializers import ArticleSerializer, ArticleCreateSerializer


def add_slug_to_question(instance):
    slug = slugify(instance.title)
    random_string = generate_random_string()
    instance.slug = slug + '-' + random_string


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter



class ArticleFeedView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        user_following = FollowingUsers.objects.filter(follower__email=user)
        users_followed_by_current_user = [following.followed for following in user_following]

        queryset = self.queryset.filter(author__in=users_followed_by_current_user).order_by('-create_date')

        return queryset


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data.get('title'):
            add_slug_to_question(instance)
            instance.save()

        return Response(serializer.data)
