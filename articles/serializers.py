from rest_framework import serializers
from .models import Article, Comment, FavoriteArticles

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'tags', 'created_date', 'last_updated', ]