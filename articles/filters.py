import django_filters
from django_filters import CharFilter

from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    author = CharFilter(field_name="author__username")
    tag = CharFilter(field_name='tags', lookup_expr="icontains")
    favorite_by = CharFilter(field_name='favorite_by__user__username')

    class Meta:
        model = Article
        fields = ['tag', 'author', 'favorite_by']
