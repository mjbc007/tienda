$.ajax({
    type: 	'GET',
    url: 	'/obtener/carrito/items/',
    data: 	{},
    success: function(data){
        $('#tag_carrito_items').text(data.total);
    },
    dataType: 'json'
});