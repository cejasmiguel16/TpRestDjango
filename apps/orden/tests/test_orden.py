from apps.orden.models import DetalleOrden, Orden
from apps.stock.models import Producto
import pytest

from apps.orden.tests.fixtures import crear_orden, crear_producto, crear_productos, api_client, crear_detalle_orden

#1
#Verificar que al ejecutar el endpoint de recuperación de una orden, se devuelven 
#los datos correctos de la orden y su detalle

@pytest.mark.django_db
def test_api_recuperar_orden(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    #detalle1 = crear_detalle_orden(orden, 15, producto1)
    #detalle1 = crear_detalle_orden(orden, 5, producto2)

    data1 = {
        "orden": orden.pk,
        "fecha_hora": orden.fecha_hora
    }

    response = client.get('/api/orden/', data = data1)
    assert response.status_code == 200
    assert Orden.objects.count() == 1

#2.
# Verificar que al ejecutar el endpoint de creación de una orden, 
# ésta se cree correctamente junto con su detalle, y que además, 
# se haya actualizado el stock de producto relacionado con un detalle de orden. 
# Se debe considerar aquí, que los datos de la orden a crear, 
# no posea productos repetidos y que la cantidad de productos en el detalle de la orden, 
# sea menor o igual al stock del producto.

@pytest.mark.django_db
def test_api_crear_DetalleOrden(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    stock_anterior = producto1.stock

    #Se actualizo el stock?
    data2={
        "orden":orden.pk,
        "cantidad": 12,
        "productos" : producto1.pk
    }
    response2 = client.post('/api/detalle/', data = data2)
    assert response2.status_code == 201
    detalle = DetalleOrden.objects.get(orden=orden, productos=producto1)
    producto = Producto.objects.get(pk=producto1.pk)
    assert stock_anterior == (producto.stock + detalle.cantidad)

#3
#Verificar que al ejecutar el endpoint de creación de una orden, se produzca un fallo al 
#intentar crear una orden cuyo detalle tenga productos repetidos. 

@pytest.mark.django_db
def test_api_crear_DetalleOrden_producto_repetido(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    stock_anterior = producto1.stock

    crear_detalle_orden(orden,1,producto1)

    data = {
        "orden":orden.pk,
        "cantidad": 10,
        "productos" : producto1.pk
    }
    response2 = client.post('/api/detalle/', data = data)
    assert response2.status_code == 400
    assert DetalleOrden.objects.filter(orden = orden.pk, productos = producto1.pk).count() == 1

# 4
# Verificar que al ejecutar el endpoint de creación de una orden, se produzca un fallo al 
# intentar crear una orden donde la cantidad de un producto del detalle, sea mayor al 
# stock de ese producto.

@pytest.mark.django_db
def test_api_productos_repetidos(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    
    data2={
        "orden":orden.pk,
        "cantidad": 21,
        "productos" : producto1.pk
    }
    response2 = client.post('/api/detalle/', data = data2)
    assert response2.status_code == 400
    assert DetalleOrden.objects.filter(orden=orden, productos=producto1).count() == 0


#5 
# Verificar que al ejecutar el endpoint de eliminación de una orden, ésta se haya eliminado de la 
# base de datos correctamente, junto con su detalle, y que además, se haga incrementado el stock de 
# producto relacionado con cada detalle de orden.

@pytest.mark.django_db
def test_api_delete_orden(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    
    data1={
        "orden":orden.pk,
        "cantidad": 15,
        "productos" : producto1.pk
    }

    data2={
        "orden":orden.pk,
        "cantidad": 1,
        "productos" : producto2.pk
    }
    
    response1 = client.post('/api/detalle/', data = data1)
    response2 = client.post('/api/detalle/', data = data2)
    assert response1.status_code == 201
    assert response2.status_code == 201

    response3 = client.delete('/api/orden/{}/'.format(orden.pk))
    assert response3.status_code == 204
    assert DetalleOrden.objects.filter(orden=orden).count() == 0
    assert Producto.objects.get(id = producto1.pk).stock == 20
    assert Producto.objects.get(id = producto2.pk).stock == 15

#Verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo 
#al total de cada detalle.

@pytest.mark.django_db
def test_api_total_orden(api_client, crear_orden, crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    
    data1={
        "orden":orden.pk,
        "cantidad": 15,
        "productos" : producto1.pk
    }

    data2={
        "orden":orden.pk,
        "cantidad": 1,
        "productos" : producto2.pk
    }
    
    response1 = client.post('/api/detalle/', data = data1)
    response2 = client.post('/api/detalle/', data = data2)
    assert response1.status_code == 201
    assert response2.status_code == 201

    detalles = DetalleOrden.objects.filter(orden = orden)
    total = 0
    for detalle in detalles:
        total += detalle.productos.precio * detalle.cantidad
    
    assert len(detalles) == 2
    assert orden.get_total() == total
