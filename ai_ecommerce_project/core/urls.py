from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet


# router to automatically generate URL patterns and corresponding http methods
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
