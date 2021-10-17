from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from pedido.models import Articulo, Compra, DetalleCompra, DetallePedido, Pedido

# Create your views here.
def ingresar(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        acceso = authenticate(request, username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.WARNING, 'Usuario no activo.')
        else:
            messages.add_message(request, messages.WARNING, 'Usuario no tiene acceso.')
    return render(request, 'login.html')


@login_required(login_url='/login/')
def catalogo(request):
    articulos = Articulo.objects.all()
    context = {
        'articulos': articulos
    }
    return render(request, 'catalogo.html',context )

@login_required(login_url='/login/')
def carrito(request):
    pedido = None
    detalle = None
    total = 0
    if request.user.is_authenticated:
        usuario = request.user
        if Pedido.objects.filter(usuario=usuario, facturado=False).exists():
            pedido=Pedido.objects.get(usuario=usuario, facturado=False)
            detalle=DetallePedido.objects.filter(pedido=pedido)
            total=DetallePedido.objects.filter(pedido=pedido).aggregate(total=Sum('subtotal'))
    return render(request, 'carrito.html', {'pedido': pedido, 'detalle_pedido':detalle, 'total':total})

@login_required(login_url='/login/')
def historial(request):
    l_compras = []
    detalles_compras = []
    if request.user.is_authenticated:
        compras = Compra.objects.filter(usuario=request.user)
        for item in compras:
            detalles_compras = DetalleCompra.objects.filter(compra=item)
            total_compra = DetalleCompra.objects.filter(compra=item).aggregate(total=Sum('subtotal'))
            o_compra = {
                'pk':item.pk,
                'fecha': item.fecha,
                'fecha_hora':item.fecha_hora,
                'usuario': item.usuario,
                'detalles':detalles_compras,
                'total_compra':total_compra
            }
            l_compras.append(o_compra)
    return render(request, 'historial.html', {'compras':l_compras})



#----------------------------- AJAX --------------------
def pedido_agregar_articulo(request):
    total_articulos = 0
    if request.is_ajax():
        if request.method == 'POST':
            usuario = request.user
            id_articulo = request.POST['id_articulo']
            cantidad = request.POST['cantidad']
            if Articulo.objects.filter(pk=id_articulo).exists():
                o_articulo = Articulo.objects.get(pk=id_articulo)
                if Pedido.objects.filter(usuario=usuario, facturado=False).exists():
                    o_pedido = Pedido.objects.get(usuario=usuario, facturado=False)
                else:
                    o_pedido = Pedido(
                        usuario=usuario
                    )
                    o_pedido.save()
                if DetallePedido.objects.filter(articulo=o_articulo, pedido=o_pedido).exists():
                    o_detalle = DetallePedido.objects.get(pedido=o_pedido, articulo=o_articulo)
                    vcantidad = o_detalle.cantidad
                    o_detalle.cantidad = float(vcantidad) + float(cantidad)
                    o_detalle.precio = o_articulo.precio
                    o_detalle.subtotal = float(o_detalle.cantidad) * float(o_articulo.precio)
                    o_detalle.save()
                else:
                    precio = o_articulo.precio
                    o_detalle = DetallePedido(
                        pedido=o_pedido,
                        articulo=o_articulo,
                        cantidad=cantidad,
                        precio=precio,
                        subtotal=float(precio) * float(cantidad)
                    )
                    o_detalle.save()
                o_articulo.cantidad = float(o_articulo.cantidad) - float(cantidad)
                o_articulo.save()
                r_articulo = {
                    'pk':o_articulo.pk,
                    'nombre':o_articulo.nombre,
                    'cantidad':o_articulo.cantidad
                }
                mensaje = "Se ha agregado el item"
                total_articulos = DetallePedido.objects.filter(pedido=o_detalle.pedido).count()
                return JsonResponse({'mensaje':mensaje, 'articulo': r_articulo, 'total_articulo':total_articulos})
            else:
                mensaje = "Articulo no existe"
        else:
            mensaje = 'Método no permitido'
    else:
        mensaje = 'Solicitud no es asíncrona.'
    data = {'mensaje': mensaje, 'total_articulos': total_articulos}
    return JsonResponse(data)

def pedido_eliminar_articulo(request):
    total = 0
    total_articulos = 0
    id_detalle = 0
    id_pedido = 0
    if request.is_ajax():
        if request.method == 'POST':
            usuario = request.user
            id_detalle = request.POST['id_detalle']
            if DetallePedido.objects.filter(pk=id_detalle).exists():
                o_detalle = DetallePedido.objects.get(pk=id_detalle)
                cantidad_detalle = o_detalle.cantidad
                id_detalle = o_detalle.pk
                pedido = o_detalle.pedido
                o_articulo = Articulo.objects.get(pk=o_detalle.articulo.pk)
                o_articulo.cantidad = float(o_articulo.cantidad) + float(cantidad_detalle)
                o_detalle.delete()
                o_articulo.save()
                vtotal=DetallePedido.objects.filter(pedido=o_detalle.pedido).aggregate(total=Sum('subtotal'))
                total = vtotal['total']
                total_articulos = DetallePedido.objects.filter(pedido=o_detalle.pedido).count()
                mensaje = "Se ha agregado el item"
                vtotal=DetallePedido.objects.filter(pedido=o_detalle.pedido).aggregate(total=Sum('subtotal'))
                total = vtotal['total']
                total_articulos = DetallePedido.objects.filter(pedido=o_detalle.pedido).count()
                return JsonResponse({'mensaje':mensaje, 'total': total, 'id_detalle': id_detalle, 'total_articulos':total_articulos})
            else:
                mensaje = "Articulo no existe"
        else:
            mensaje = 'Método no permitido'
    else:
        mensaje = 'Solicitud no es asíncrona.'
    data = {'mensaje': mensaje}
    return JsonResponse(data)

def pedido_actualizar_detalle(request):
    r_detalle=None
    total = 0
    if request.is_ajax():
        if request.method == 'POST':
            id_detalle = request.POST['id_detalle']
            cantidad = request.POST['cantidad']
            if DetallePedido.objects.filter(pk=id_detalle).exists():
                mensaje = "Se ha actualizado el registro"
                o_detalle = DetallePedido.objects.get(pk=id_detalle)
                cantidad_detalle = float(o_detalle.cantidad)
                o_detalle.cantidad = float(cantidad)
                o_detalle.subtotal = float(o_detalle.cantidad) * float(o_detalle.articulo.precio)
                o_detalle.save()
                o_articulo = Articulo.objects.get(pk=o_detalle.articulo.pk)
                cantidad_articulo = float(o_articulo.cantidad)
                print(cantidad)
                print(cantidad_articulo)
                print(cantidad_detalle)
                if cantidad_detalle > float(cantidad):
                    o_articulo.cantidad = cantidad_articulo + (cantidad_detalle - float(cantidad))
                else:
                    o_articulo.cantidad = cantidad_articulo - (float(cantidad) - cantidad_detalle)
                o_articulo.save()
                r_detalle = {
                    'pk':o_detalle.pk,
                    'cantidad':o_detalle.cantidad
                }
                vtotal=DetallePedido.objects.filter(pedido=o_detalle.pedido).aggregate(total=Sum('subtotal'))
                total = vtotal['total']
            else:
                mensaje="No existe el registro"
            return JsonResponse({'mensaje':mensaje, 'detalle': r_detalle, 'total':total})
        else:
            mensaje = 'Método no permitido'
    else:
        mensaje = 'Solicitud no es asíncrona.'
    data = {'mensaje': mensaje}
    return JsonResponse(data)

def total_items_carrito(request):
    total = 0
    if request.is_ajax():
        if request.user.is_authenticated:
            usuario = request.user
            if Pedido.objects.filter(usuario=usuario, facturado=False).exists():
                o_pedido = Pedido.objects.get(usuario=usuario, facturado=False)
                total = DetallePedido.objects.filter(pedido=o_pedido).count()
    data = {
        'total':total
    }
    return JsonResponse(data)

def facturar_pedido(request):
    data= {}
    error = False
    total = 0
    mensaje = "Se ha facturado el pedido"
    if request.is_ajax():
        if request.user.is_authenticated:
            usuario = request.user
            id_pedido = request.POST['id_pedido']
            if Pedido.objects.filter(pk=id_pedido).exists():
                o_pedido = Pedido.objects.get(pk=id_pedido)
                o_compra = Compra(
                    pedido = o_pedido,
                    usuario=usuario
                )
                o_compra.save()
                o_detalle = DetallePedido.objects.filter(pedido=o_pedido)
                for item in o_detalle:
                    o_detalle_compra = DetalleCompra(
                        compra=o_compra,
                        articulo=item.articulo,
                        cantidad = item.cantidad,
                        precio=item.precio,
                        subtotal=item.subtotal
                    )
                    o_detalle_compra.save()
                o_pedido.facturado=True
                o_pedido.save()
            else:
                mensaje = "No existe pedido"
                error = True
            if Pedido.objects.filter(usuario=usuario, facturado=False).exists():
                o_pedido = Pedido.objects.get(usuario=usuario, facturado=False)
                total = DetallePedido.objects.filter(pedido=o_pedido).count()
    data = {
        'mensaje': mensaje,
        'error': error,
        'total_articulos':total
    }
    return JsonResponse(data)