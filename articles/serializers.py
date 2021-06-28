from rest_framework import serializers

from users.serializers import UserProfileSerializer
from .models import Article, Comment, FavoriteArticles


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'description', 'body', 'tags']


class ArticleSerializer(serializers.ModelSerializer):
    favorites_count = serializers.SerializerMethodField(read_only=True)
    favorited = serializers.SerializerMethodField(read_only=True)
    tagList = serializers.ListField(child=serializers.CharField(), source="tags", read_only=True)
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Article
        exclude = ['id', 'tags']

    def get_created_at(self, instance):
        return instance.create_date.strftime('%B %d, %Y')

    def get_updated_at(self, instance):
        return instance.last_updated.strftime('%B %d, %Y')

    def get_favorites_count(self, instance):
        return instance.favorite_by.count()

    def get_favorited(self, instance):
        request = self.context.get('request')
        return instance.favorite_by.filter(user=request.user).exists()


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'create_date', 'last_updated', 'body', 'author']
