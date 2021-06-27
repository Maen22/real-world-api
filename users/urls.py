from django.urls import path

from users.views import CreateUserView, \
    CreateTokenView, \
    ManageUserView, \
    UserProfileView, \
    FollowUsersView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<str:username>/follow/', FollowUsersView.as_view(), name='user-profile-follow'),
]
