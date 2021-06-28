from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import generate_random_string
from users.models import FollowingUsers
from .filters import ArticleFilter
from .models import Article, FavoriteArticles, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer


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


class FavoriteArticleAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)

        if FavoriteArticles.objects.filter(article=article, user=request.user):
            raise ValidationError("The article is already in your favorites list.")

        favorite_article = FavoriteArticles()

        favorite_article.article = article
        favorite_article.user = self.request.user
        favorite_article.save()

        return Response({'message': f'Article with ID: {article.pk} added to favorites.'})

    def delete(self, request, slug):
        article = Article.objects.filter(slug=slug)[0]

        if not FavoriteArticles.objects.filter(article=article, user=request.user):
            raise ValidationError("The article is already not of your favorites.")

        favorite_article = FavoriteArticles.objects.filter(article=article, user=self.request.user)[0]
        favorite_article.delete()

        return Response({'message': f'Article with ID: {article.pk} removed from favorites.'})


class CommentAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        comments = Comment.objects.filter(article__slug=slug)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)

        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user, article=article)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def delete(self, request, slug, pk):
        comment = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
