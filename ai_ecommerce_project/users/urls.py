from django.urls import path
from .views import RegisterUserView, UserProfileView, CustomAuthToken


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('me', UserProfileView.as_view(), name='user-profile'),
    path('login/', CustomAuthToken.as_view(), name='user-login'),
]
