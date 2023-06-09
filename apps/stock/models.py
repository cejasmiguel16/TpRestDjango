from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    precio = models.FloatField(null=False)
    stock = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.nombre} hay {self.stock} en stock"

