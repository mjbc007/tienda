$('.card-body').on('click', '.btnEditar', function(e){
    e.preventDefault();
    var id_detalle = $(this).attr('data');
    var cantidad = parseFloat($(this).attr('data-c'));
    html = '<input type="number" id="txtEdita_'+id_detalle+'" class="text-center" name="cantidad" value="'+cantidad+'" style="width: 75px;"> '
    html += '<a href="#" class="btnActualizarCantidad" data="'+id_detalle+'">Actualizar</a>'
    $('#editar_' + id_detalle).html(html);
});

$('.card-body').on('click','.btnActualizarCantidad', function(e) {
    e.preventDefault();
    var id_detalle = $(this).attr('data');
    var cantidad = $('#editar_'+id_detalle+'>#txtEdita_'+id_detalle).val();
    $.ajax({
        type:'POST',
        url:'/pedido/actualizar/articulo/',
        data: {
            'id_detalle':id_detalle,
            'cantidad': cantidad,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            html ="<span>Cantidad: "+data.detalle.cantidad+"</span> "
            html+="<a href='#' data="+data.detalle.pk+" data-c="+data.detalle.cantidad+" class='btnEditar'>Editar</a>"
            $('#editar_' + data.detalle.pk).html(html);
            $('#tag_total').html(data.total);
        },
        dataType: 'json',
    });
});

$('.card-body').on('click','.btnEliminar', function(e) {
    e.preventDefault();
    var id_detalle = $(this).attr('data');
    $.ajax({
        type:'POST',
        url:'/pedido/eliminar/articulo/',
        data: {
            'id_detalle':id_detalle,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            if (data.id_detalle > 0) {
                $('#detalle_'+data.id_detalle).slideUp('slow');
                $('#tag_total_items').text(data.total_articulos);
            }
            if (data.total_articulos === 0) {
                html = "<h3 class='h3'>No hay productos en carrito</h3>"
                $(html).insertAfter('.row>h2');
                $('#tag_suma_total').remove();
                $('#tag_boton_pago').remove();
            }
            $('#tag_total').html(data.total);
            $('#tag_carrito_items').text(data.total_articulos);
        },
        dataType: 'json',
    });
});
$('#tag_boton_pago>a').on('click', function(e) {
    e.preventDefault();
    var id_pedido = $(this).attr('data');
    $.ajax({
        type:'POST',
        url:'/pedido/facturar/',
        data: {
            'id_pedido':id_pedido,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            if (data.error === false) {
                $('.btnEliminar').remove();
                $('.btnEditar').remove();
                $('#tag_boton_pago').remove();
                $('<h3 class="h3 alert alert-success" role="alert">Su pedido ha sido facturado. Verifique el historial de compras.</h3>').insertAfter('.row>h2');
                $('#tag_carrito_items').text(data.total_articulos);
            }
        },
        dataType: 'json',
    });
})