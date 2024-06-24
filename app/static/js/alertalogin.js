
document.addEventListener("DOMContentLoaded", function() {
    var botonOpinion = document.querySelector('.alerta-login');
    if(botonOpinion) {
        
        botonOpinion.addEventListener('click', function(event) {
            event.preventDefault(); // Evita que el botón siga su comportamiento por defecto (navigación)
            alert("Antes de opinar primero inicia sesión");
            window.location.href ="/login";
        });
    }
});

