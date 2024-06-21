from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager
from functools import wraps
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
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
            print(request.form)
            username = request.form ['txt']
            email = request.form['Email']
            password = request.form['pswd']


            if not username or not email or not password:
                flash('Por favor, completa todos los campos.', 'danger')
                return render_template('register.html')
            
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            cursor = db.cursor()
            query = "INSERT INTO Registro (Nombre_Cliente, Email_Cliente, Contraseña_Usuario) VALUES (%s, %s, %s)"
            values = (username, email, hashed_password)
            cursor.execute(query, values)
            db.commit()

            flash('Usuario registrado correctamente!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']
        role = request.form['role'] 

        cursor = db.cursor()
        query = "SELECT * FROM Registro WHERE Email_Cliente = %s AND Rol_Usuario = %s"
        cursor.execute(query, (email, role))
        user = cursor.fetchone()
        

        stored_hash = user[3]

        validacion = check_password_hash(stored_hash, password)
        print("Aca esta la validacion: ", validacion)

        if validacion:
            session['user_id'] = user[0]
            flash('Inicio de sesion exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            print("Error en la validacion de la contraseña")
            flash('Correo electronico, contraseña o rol incorrectos.', 'danger')
    else:
        print("Usuario no encontrado")

    return render_template('login.html')

@app.route('/index', methods = ['GET', 'POST']) 
def index():
    
        return render_template('index.html')

@app.route('/about') 
def about():
    return render_template('about.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


logging.basicConfig(level=logging.DEBUG)

@app.route('/reservation', methods= ['GET', 'POST'])
def reservation():
    
    print("En la página web.")
    
    if request.method == 'POST':
        
        print("Si entra :)")
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
            return redirect(url_for('success'))
        
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