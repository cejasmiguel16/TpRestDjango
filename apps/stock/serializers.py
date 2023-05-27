from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['stock']
    
    def update(self, instance, validated_data):
        # Solo se permite modificar el campo 'stock'
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance