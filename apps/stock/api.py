from .models import Producto
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import ProductoSerializer, ProductoStockSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return ProductoStockSerializer
        else:
            return ProductoSerializer
