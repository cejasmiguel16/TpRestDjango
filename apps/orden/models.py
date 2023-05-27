from django.db import models
from apps.stock.models import Producto

# Create your models here.

class Orden(models.Model):
    fecha_hora = models.DateTimeField(null=False)

class DetalleOrden(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)