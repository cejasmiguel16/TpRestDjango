from django.db import models
from apps.stock.models import Producto
from django.db.models import Sum,F
from django.db.models.functions import Cast

# Create your models here.

class Orden(models.Model):
    fecha_hora = models.DateTimeField(null=False)

    def get_total(self):
        total = DetalleOrden.objects.filter(orden=self).aggregate(
            total=Sum(F('productos__precio') * F('cantidad'))
            )['total'] or 0

        return total

    def __str__(self):
        return f"Orden #{self.id} pedida en: {self.fecha_hora}"

    
    
class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)