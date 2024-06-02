var prenda_Label = document.querySelector('#Cargar_Penda_Div input[type="file"]');
var categoria_Label = document.querySelector('#Categoria_Div');
prenda_Label.addEventListener('change', function() {
    if (prenda_Label.files.length > 0) {
        categoria_Label.innerHTML = '<input type="text" name="categoria" value="camiseta" />';
    } 
});
