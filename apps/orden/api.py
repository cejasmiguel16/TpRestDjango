from xml.dom import ValidationErr
from apps.orden.models import Orden, DetalleOrden
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import OrdenSerializer, DetalleOrdenSerializer

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

    def perform_create(self, serializer):
        producto = serializer.validated_data.get('productos', None)
        cantidad = serializer.validated_data.get('cantidad', None)
        total = producto.stock - cantidad
        if total < 0:
            raise ValidationErr("no hay stock suficiente")
        producto.stock -= cantidad
        producto.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, serializer):
        producto = self.get_object().productos
        cantidad = self.get_object().cantidad
        producto.stock += cantidad
        producto.save()
        super().perform_destroy(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        producto = self.get_object().productos
        cantidad = self.get_object().cantidad
        totalStock = producto.stock + cantidad
        cantidadPedida = serializer.validated_data.get('cantidad', None)
        if totalStock - cantidadPedida < 0:
           raise ValidationErr("no hay stock suficiente")

        elif totalStock - cantidadPedida >= 0:
            producto.stock = (totalStock - cantidadPedida)
            producto.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    