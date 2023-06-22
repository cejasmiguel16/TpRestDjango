from apps.stock.models import Producto
import pytest

from apps.orden.tests.fixtures import  api_client

#6
#Verificar que al ejecutar el endpoint de modificación del stock de un producto, 
#actualiza correctamente dicho stock.

@pytest.mark.django_db
def test_api_modificar_stock(api_client):
    client = api_client
    
    data = {
        "nombre" : "Camiseta",
        "stock" : 40,
        "precio" : 2000
    }

    response = client.post('/api/producto/', data = data)
    assert Producto.objects.count() == 1

    data2 = {
        "stock" : 20
    }
    response2 = client.patch('/api/producto/1/' , data = data2)
    assert Producto.objects.count() == 1
    producto = Producto.objects.get(id = 1)
    assert producto.stock == 20




