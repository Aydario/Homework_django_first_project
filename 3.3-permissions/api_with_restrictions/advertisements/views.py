from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter


class IsOwnerOrReadOnly(BasePermission):
    """Только владелец может изменять/удалять объект."""

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        # Изменение/удаление — только владельцу
        return obj.creator == request.user


class IsAdminOrReadOnly(BasePermission):
    """Только администратор может изменять/удалять объект."""

    def has_permission(self, request, view):
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        # Изменение/удаление — только администратору
        return request.user.is_staff


class CanViewDraft(BasePermission):
    """Черновики видит только автор."""

    def has_object_permission(self, request, view, obj):
        # Черновик виден только автору
        if obj.status == 'DRAFT':
            return obj.creator == request.user
        return True


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """Получение queryset с учетом статуса DRAFT."""

        user = self.request.user

        # Админ видит все объявления
        if user.is_staff:
            return Advertisement.objects.all()

        # Авторизованный пользователь видит свои черновики и все открытые/закрытые
        if user.is_authenticated:
            return Advertisement.objects.filter(
                models.Q(status__in=['OPEN', 'CLOSED']) | models.Q(creator=user)
            )

        # Анонимный пользователь видит только открытые/закрытые
        return Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        elif self.action in ["list", "retrieve"]:
            return [AllowAny(), CanViewDraft()]
        return []

    def perform_create(self, serializer):
        """Создание объявления с простановкой автора."""
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Закрыть объявление."""
        advertisement = self.get_object()
        advertisement.status = 'CLOSED'
        advertisement.save()
        return Response({'status': 'CLOSED'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def open(self, request, pk=None):
        """Открыть объявление."""
        advertisement = self.get_object()
        advertisement.status = 'OPEN'
        advertisement.save()
        return Response({'status': 'OPEN'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        """Добавить объявление в избранное."""
        advertisement = self.get_object()

        # Нельзя добавить своё объявление в избранное
        if advertisement.creator == request.user:
            return Response(
                {"detail": "Нельзя добавить своё объявление в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.favorites.add(request.user)
        return Response(
            {"detail": "Объявление добавлено в избранное"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def remove_from_favorites(self, request, pk=None):
        """Удалить объявление из избранного."""
        advertisement = self.get_object()
        advertisement.favorites.remove(request.user)
        return Response(
            {"detail": "Объявление удалено из избранного"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Получить список избранных объявлений."""
        favorite_ads = Advertisement.objects.filter(favorites=request.user)
        serializer = self.get_serializer(favorite_ads, many=True)
        return Response(serializer.data)
