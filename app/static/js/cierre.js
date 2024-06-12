function confirmLogout() {
    if (confirm("¿Estás seguro de que quieres cerrar la sesión?")) {
        window.location.href = "/login";
        alert("Sesión cerrada");
    } else {
        alert("Operación cancelada");
    }
}

function cancelLogout() {
    alert("Operación cancelada");
}