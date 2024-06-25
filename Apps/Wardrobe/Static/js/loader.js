document.getElementById("myForm").addEventListener("submit", function(event) {
    // Mostrar el loader al enviar el formulario
    document.getElementById("loader").style.display = "block";
    
    // Ocultar los elementos especificados
    document.getElementById("mainContent").style.display = "none";
});


