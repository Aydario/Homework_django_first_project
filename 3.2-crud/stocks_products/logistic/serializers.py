from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции продукта на складе"""
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада с вложенными позициями"""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        """Создание склада с позициями"""
        positions = validated_data.pop('positions')
        
        # Создаем склад
        stock = Stock.objects.create(**validated_data)
        
        # Создаем позиции для склада
        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
        
        return stock

    def update(self, instance, validated_data):
        """Обновление склада с позициями"""
        positions = validated_data.pop('positions')
        
        # Обновляем склад
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем или создаем позиции
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=instance,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                }
            )
        
        return instance
        