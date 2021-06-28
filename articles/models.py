from django.conf import settings
from django.contrib.postgres import fields
from django.db import models
from django.db.models import Manager

from core.models import AuditableModel


class Article(AuditableModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=50)
    description = models.TextField()
    body = models.TextField()
    tags = fields.ArrayField(
        models.CharField(max_length=50, null=False, blank=False)
    )

    def __str__(self):
        return self.title


class Comment(AuditableModel):
    body = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
                                related_name='comments',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class FavoriteArticles(AuditableModel):
    article = models.ForeignKey(
        Article, related_name="favorite_by", on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorite_articles", on_delete=models.CASCADE)

    objects = Manager()

    class Meta:
        unique_together = (
            "article",
            "user",
        )

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'
