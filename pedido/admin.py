from django.contrib import admin
from .models import Articulo, Compra, DetalleCompra, DetallePedido, Pedido

# Register your models here.
admin.site.register(Articulo)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Compra)
admin.site.register(DetalleCompra)