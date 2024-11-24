from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        """Handles POST operations, validates through serializer, saves to db, return new product object"""
        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,  # filtering based on specific fields
        filters.SearchFilter,  # search func
        filters.OrderingFilter  # sorting func
    ]

    filterset_fields = ['category', 'price', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'rating', 'created_at']

    def create(self, request, *args, **kwargs):
        """Handles POST operations, validates through serializer, saves to db, return new product object"""
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Returns a list of featured products, serialising them as JSON"""
        featured_products = Product.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """Returns a list of top-rated products"""
        top_rated_products = Product.objects.order_by('-rating')[:10]
        serializer = self.get_serializer(top_rated_products, many=True)
        return Response(serializer.data)
