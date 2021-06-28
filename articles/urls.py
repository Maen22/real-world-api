from django.urls import path

from .views import ArticleListView, ArticleFeedView, ArticleCreateView, ArticleRUDView, FavoriteArticleAPIView, \
    CommentAPIView, CommentDeleteAPIView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('feed/', ArticleFeedView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<slug:slug>/', ArticleRUDView.as_view(), name='article-RUD'),
    path('<slug:slug>/favorite/', FavoriteArticleAPIView.as_view(), name='article-favorite'),
    path('<slug:slug>/comments/', CommentAPIView.as_view(), name='comment-list-create'),
    path('<slug:slug>/comments/<int:pk>/', CommentDeleteAPIView.as_view(), name='comment-delete'),
]
