"""tienda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pedido import views as pedido_url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pedido_url.catalogo, name='catalogo'),
    path('carrito/', pedido_url.carrito, name='carrito'),
    path('historial/', pedido_url.historial, name='historial'),
    path('login/', pedido_url.ingresar, name='ingresar'),

    #--------------------AJAX----------------------
    path('pedido/agregar/articulo/', pedido_url.pedido_agregar_articulo, name='pedido_agregar_articulo'),
    path('pedido/actualizar/articulo/', pedido_url.pedido_actualizar_detalle, name='pedido_actualizar_detalle'),
    path('pedido/eliminar/articulo/', pedido_url.pedido_eliminar_articulo, name='pedido_eliminar_articulo'),
    path('obtener/carrito/items/', pedido_url.total_items_carrito, name='total_items_carrito'),
    path('pedido/facturar/', pedido_url.facturar_pedido, name='facturar_pedido'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
