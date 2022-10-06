from pyexpat import model
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ["name"]

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class= BrandSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ["name"]

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    filter_backend = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ["category", "brand"]
    search_fields = ["name"]