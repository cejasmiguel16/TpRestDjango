from django.urls import path
from rest_framework import routers
from apps.orden.api import DetalleOrdenViewSet, OrdenViewSet
from apps.stock.api import ProductoViewSet

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()
# Registrar un ViewSet
router.register(prefix='orden', viewset=OrdenViewSet)
router.register(prefix='producto', viewset=ProductoViewSet)
router.register(prefix='detalle', viewset=DetalleOrdenViewSet)


urlpatterns = []
urlpatterns += router.urls