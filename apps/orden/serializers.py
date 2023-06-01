from rest_framework import serializers
from .models import Orden,DetalleOrden
import requests

class OrdenSerializer(serializers.ModelSerializer):
    total_pedido = serializers.SerializerMethodField(method_name='get_total_pedido')
    total_usd = serializers.SerializerMethodField(method_name='get_total_usd')

    class Meta:
        model = Orden
        fields = '__all__'
        read_only_fields = ['total_pedido', 'total_usd']

    def get_total_usd(self, obj):
        url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
        response = requests.get(url)

        # Obtener el JSON de la respuesta
        data = response.json()

        # Buscar la cotización del dólar blue en los datos
        for cotizacion in data:
            if cotizacion["casa"]["nombre"] == "Dolar Blue":
                precio_venta = float(cotizacion["casa"]["venta"].replace(",", "."))
                precio_compra = float(cotizacion["casa"]["compra"].replace(",", "."))

        total_usd = round((obj.get_total() / precio_venta),2)
        total_usd_str = "$"+str(total_usd)
        return total_usd_str

    def get_total_pedido(self, obj):
        return obj.get_total()

class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = '__all__'