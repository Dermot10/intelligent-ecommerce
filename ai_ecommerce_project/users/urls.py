from django.urls import path
from .views import RegisterUserView, UserProfileView, UserListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('list-users/', UserListView.as_view(), name='user-list'),
]
