from rest_framework import serializers
from .models import Article, Comment, FavoriteArticles


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    favoritesCount = serializers.SerializerMethodField(read_only=True)
    favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article

    def get_created_at(self, instance):
        return instance.created_at.strftime('%B %d, %Y')

    def get_updated_at(self, instance):
        return instance.created_at.strftime('%B %d, %Y')

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get('request')
        return instance.answers.filter(author=request.user).exists()
