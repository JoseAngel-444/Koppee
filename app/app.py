from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, current_user
from functools import wraps
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort
import os
import logging


basedir = os.path.abspath(os.path.dirname(__file__))
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'koppe2')
}

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = '08400840'

app.config['WerkzeugSecurityHashMethod'] = 'sha256'

db = mysql.connector.connect(**db_config)

class Usuario:
    def __init__(self, id, nombrecli, email):
        self.id = id
        self.nombrecli = nombrecli
        self.email = email

class Comentario:
    def __init__(self, id, texto, usuario_id, fecha_creacion):
        self.id = id
        self.texto = texto
        self.usuario_id = usuario_id
        self.fecha_creacion = fecha_creacion
        

@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor()
    query = "SELECT * FROM Registro WHERE 	ID_Registro = %s"
    cursor.execute(query, (user_id))
    user_data = cursor.fetchone()

    if user_data:
        user = Usuario (id=user_data[0], nombrecli=user_data[2], email=user_data[4])
        return user
    else:
        return None

    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Debes iniciar sesión primero.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
def register():

        if request.method == 'POST':

            username = request.form ['txt']
            email = request.form['Email']
            password = request.form['pswd']


            if not username or not email or not password:
                type_Flash = "alert-danger"
                flash('Por favor, completa todos los campos.')
            
            cursor = db.cursor()
            query = "SELECT * FROM Registro WHERE (Email_Cliente = %s OR Nombre_Cliente = %s) AND Rol_Usuario = 'cliente' "
            cursor.execute(query, (email, username))
            user = cursor.fetchone()
            
            if user is None:
                
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                cursor = db.cursor()
                query = "INSERT INTO Registro (Nombre_Cliente, Email_Cliente, Contraseña_Usuario) VALUES (%s, %s, %s)"
                values = (username, email, hashed_password)
                cursor.execute(query, values)
                db.commit()
                
                type_Flash = "alert-success"
                flash('Usuario registrado correctamente!')
            
            else:
                
                cursor = db.cursor()
                query = "SELECT Email_Cliente FROM Registro WHERE Email_Cliente = %s AND Rol_Usuario = 'cliente' "
                cursor.execute(query, (email,))
                Is_Available_Email = cursor.fetchone()
                type_Flash = "alert-danger"
                
                if Is_Available_Email and Is_Available_Email[0] == email:
                
                    print("Email ya tomado. ")
                    flash("El email ingresado ya esta en uso. ")
                
                elif Is_Available_Email and Is_Available_Email[0] != email:
                
                    print("Nombre de usuario ya tomado. ")
                    flash("El nombre de usuario ingresado ya esta en uso. ")
            
                else:
                    print("El usuario ya esta registrado en el sistema. ")
                    flash("Nombre de usuario e email ya registrados")
                    
        return render_template('login.html', type_Flash=type_Flash)


@app.route('/login', methods=['GET', 'POST'])
def login():
    type_Flash = "alert"
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['pswd']
        role = request.form['role'] 

        cursor = db.cursor()
        query = "SELECT * FROM Registro WHERE Email_Cliente = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        if user is not None:

            stored_hash = user[3]
            validacion = check_password_hash(stored_hash, password)
            print("Aca esta la validacion: ", validacion)

            if validacion:
                if user[4] == role:
                    session['ID_Registro'] = user[0]
                    session['User'] = user[1]
                    session['Type_User'] = user[4]
                
                if user[4] == 'administrador':
                    
                    type_Flash = "alert-success"
                    flash('Inicio de sesion exitoso!')
                    return redirect(url_for('Admin_View'));
                
                else:
                    type_Flash = "alert-success"
                    flash('Inicio de sesion exitoso!')
                    return redirect(url_for('index'))
            
            else:
                type_Flash = "alert-danger"
                print("Error en la validacion de la contraseña")
                flash("Contraseña incorrecta. ")
                
        else:
            
            type_Flash = "alert-danger"
            flash("Usuario no registrado.")
            print("Usuario no registrado. ")


    return render_template('login.html', type_Flash=type_Flash)


@app.route('/', methods = ['GET', 'POST']) 
def index():
    
        return render_template('index.html')

@app.route('/comentarios', methods= ['GET', 'POST'])
def comentarios():
    if not current_user.is_authenticated:
        
        if request.method == 'POST':
            texto = request.form['texto']
            comentario = Comentario(texto=texto, usuario_id=session['ID_Registro'])
            cursor = db.cursor()
            query = "INSERT INTO Comentarios (texto,usuario_id) VALUES (%s, %s)"
            values = (texto, session['ID_Registro'])
            cursor.execute(query, values)
            db.commit()
            return redirect(url_for('login'))
        comentarios = []
        cursor = db.cursor()
        query = "SELECT * FROM Comentarios"
        cursor.execute(query)
        for row in cursor.fetchall():
            comentarios.append(Comentario(row[0], row[1], row[2], row[3]))
        return render_template('Comentarios.html', comentarios=comentarios)

@app.route('/comentarios/<int:comentario_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.usuario_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        texto = request.form['texto']
        comentario.texto = texto
        cursor = db.cursor()
        query = "UPDATE Comentarios SET texto = %s WHERE id = %s"
        values = (texto, comentario_id)
        cursor.execute(query, values)
        db.commit()
        return redirect(url_for('comentarios'))
    return render_template('edit_comentarios.html', comentario=comentario)


@app.route('/comentarios/<int:comentario_id>/delete', methods=['POST'])
@login_required
def delete_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.usuario_id != current_user.id:
        abort(403)
    cursor = db.cursor()
    query = "DELETE FROM Comentarios WHERE id = %s"
    values = (comentario_id,)
    cursor.execute(query, values)
    db.commit()
    return redirect(url_for('comentarios'))

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/vision')
def mi_vision():
    return render_template('vision.html')

@app.route('/loginreserva')
def login_reserva():
    return render_template('loginreserva.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')


logging.basicConfig(level=logging.DEBUG)

@app.route('/reservation', methods= ['GET', 'POST'])
def reservation():

    
    if request.method == 'POST':
        
        Nombre_User = request.form['Name_Form']
        Email_User = request.form['Email_Form']
        Fecha_Reserva = request.form['Date_Form']
        Hora_Reserva = request.form['Hora_Form']
        Num_Personas_Reserva = request.form['Num_Personas']

        cursor = db.cursor()
        query = "SELECT * FROM Registro WHERE Email_Cliente = %s AND Nombre_Cliente = %s;"
        cursor.execute(query, (Email_User, Nombre_User))
        user = cursor.fetchone()
        
        print(Email_User, " ", Nombre_User)
        
        print(user)
        
        if user is None:
            
            print("Usuario No encontrado, verifique que el correo y contraseña sean validos. ")
            
        else:
            
            print("Si entra al else.  :D .")
            ID_User = user[0]
            
            cursor = db.cursor()
            query = "INSERT INTO Reservas (Cantidad_De_Sillas, Hora_Reserva, Fecha_Reserva, Cliente_ID_F) VALUES (%s, %s, %s, %s)"
            values = (Num_Personas_Reserva, Hora_Reserva, Fecha_Reserva, ID_User)
            cursor.execute(query, values)
            db.commit()

            flash('Reserva creada exitosamente!', 'success')
            return redirect(url_for(''))
        
    return render_template('reservation.html')

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')


@app.route('/service')
def servicio():
    return render_template('service.html')


@app.route('/sabermas1')
def saber_mas():
    return render_template('sabermas1.html')


@app.route('/logout', methods= ['GET', 'POST'])
def logout():
    # Aquí va el código para cerrar la sesión del usuario
    return render_template('logout.html')





app.run(debug=True, port=5005)