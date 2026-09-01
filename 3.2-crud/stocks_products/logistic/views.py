from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    """CRUD для продуктов с поиском по названию и описанию"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    pagination_class = PageNumberPagination


class StockViewSet(ModelViewSet):
    """CRUD для складов с фильтрацией по продуктам"""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description', 'address']
    ordering_fields = ['id', 'address']
    pagination_class = PageNumberPagination
    