import pytest

from apps.orden.models import Orden, DetalleOrden
from apps.stock.models import Producto

@pytest.fixture(scope='session')
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def crear_orden():
    orden, _ = Orden.objects.get_or_create(
        defaults={
            'fecha_hora': "2024-06-03T13:08:00Z"
        }
    )
    return orden

def crear_producto(nombre, precio, stock):
    producto, _ = Producto.objects.get_or_create(
        nombre = nombre,
        precio = precio,
        stock = stock,
    )
    return producto

def crear_detalle_orden(orden, cantidad, productos):
    detalle_orden, _ = DetalleOrden.objects.get_or_create(
        orden = orden,
        cantidad = cantidad,
        productos = productos,
    )
    

@pytest.fixture
def crear_productos():
    producto1 = crear_producto('Camiseta River', 2000, 20)
    producto2 = crear_producto('Jean Negro', 2000, 10)
    return producto1, producto2




