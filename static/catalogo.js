var btnGuardar = $('.btn');

btnGuardar.on('click', function(e){
    e.preventDefault();
    var id = $(this).attr('data');
    $.ajax({
        type:'POST',
        url:'/pedido/agregar/articulo/',
        data: {
            'id_articulo':$(this).attr('data'),
            'cantidad': 1,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            $('#precio_' + data.articulo.pk).text('Stock: '+ data.articulo.cantidad);
            $('#tag_carrito_items').text(data.total_articulo);
        },
        dataType: 'json',
    });
});