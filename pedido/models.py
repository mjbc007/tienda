from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField("Nombre", max_length=250)
    imagen = models.ImageField("Imagen", upload_to='articulos')
    precio = models.DecimalField("Precio", max_digits=18, decimal_places=2)
    cantidad = models.DecimalField("Cantidad", max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    """Model definition for Pedido."""

    fecha_hora = models.DateTimeField("Fecha y Hora", auto_now_add=True)
    fecha = models.DateField("Fecha", auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    facturado = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Pedido."""

        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        """Unicode representation of Pedido."""
        return self.usuario.username + "- Pedido No. " + str(self.pk)

class DetallePedido(models.Model):
    """Model definition for DetallePedido."""
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    cantidad = models.DecimalField("Cantidad", max_digits=18, decimal_places=2)
    precio = models.DecimalField("Precio", max_digits=18, decimal_places=2)
    subtotal = models.DecimalField("Subt", max_digits=5, decimal_places=2)

    class Meta:
        """Meta definition for DetallePedido."""

        verbose_name = 'DetallePedido'
        verbose_name_plural = 'DetallePedidos'

    def __str__(self):
        """Unicode representation of DetallePedido."""
        return "Pedido No. " + str(self.pedido.pk) + " - " + self.articulo.nombre

class Compra(models.Model):
    """Model definition for Compra."""
    fecha_hora = models.DateTimeField("Fecha y Hora", auto_now_add=True)
    fecha = models.DateField("Fecha", auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    class Meta:
        """Meta definition for Compra."""

        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        """Unicode representation of Compra."""
        return "Compra No. " + str(self.pk)

class DetalleCompra(models.Model):
    """Model definition for DetalleCompra."""
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    cantidad = models.DecimalField("Cantidad", max_digits=18, decimal_places=2)
    precio = models.DecimalField("Precio", max_digits=18, decimal_places=2)
    subtotal = models.DecimalField("Subt", max_digits=5, decimal_places=2)

    class Meta:
        """Meta definition for DetalleCompra."""

        verbose_name = 'DetalleCompra'
        verbose_name_plural = 'DetalleCompras'

    def __str__(self):
        """Unicode representation of DetalleCompra."""
        return "Pedido No. " + str(self.compra.pk) + " - " + self.articulo.nombre
