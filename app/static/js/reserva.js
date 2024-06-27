function checkLogin() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/is_logged_in', true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      if (!response.logged_in) {
        alert('Usuario no registrado');
        return false; // Evita que se envíe el formulario
      }
    }
  };
  xhr.send();
  return true; // Permite que se envíe el formulario si el usuario está logueado
}