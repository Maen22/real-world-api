from django.contrib import admin

from articles.models import Comment, Article, FavoriteArticles

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(FavoriteArticles)
