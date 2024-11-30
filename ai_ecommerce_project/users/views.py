from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Customer
from .serializers import UserSerializer, CustomerSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound("No users found.")
        return super().list(request, *args, **kwargs)

# class DeleteUserView(APIView):

#     def delete(self, request, *args, **kwargs):
#         try: 
#             user = request.user 
#             user.delete()
#             return Response({"message": "User deleted"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAuthToken(TokenObtainPairView):
    """
    Custom Token Authentication View for JWT
    """
    def post(self, request, *args, **kwargs):
        # Use TokenObtainPairView to handle token creation
        response = super().post(request, *args, **kwargs)

        # The response from `super().post()` will contain the access and refresh tokens
        return response
