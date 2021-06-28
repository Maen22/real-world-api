from django.urls import path

from .views import ArticleListView, ArticleFeedView, ArticleCreateView, ArticleRUDView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('feed/', ArticleFeedView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<slug:slug>/', ArticleRUDView.as_view(), name='article-RUD')
]
