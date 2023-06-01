from django.db import models
from apps.stock.models import Producto

# Create your models here.

class Orden(models.Model):
    fecha_hora = models.DateTimeField(null=False)

    def get_total(self):
        total = 0
        detalle_ordenes = DetalleOrden.objects.all()
        for detalle_orden in detalle_ordenes:
            if detalle_orden.orden == self:
                total += detalle_orden.productos.precio*detalle_orden.cantidad

        return total

    def __str__(self):
        return f"Orden #{self.id} pedida en: {self.fecha_hora}"

    
    
class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)