from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomAuthToken

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='token_obtain_pair'),  # POST /api/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # POST /api/token/refresh/
]
