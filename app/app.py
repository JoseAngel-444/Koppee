from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
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
    'database': os.getenv('DB_NAME', 'Koppe2')
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
    query = "SELECT * FROM Registro WHERE ID_Registro = %s"
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


@app.route('/register', methods=['POST'])
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

            #Acá se declara de una vez la clase para el error ya que si entra al else significa
            #que existe un usuario registrado ya sea con el nombre, email o ambos. 
            #Por lo cual se declara de una vez para que déspues las posibles variaciones
            #Contengan esta clase.

            type_Flash = "alert-danger"    


            cursor = db.cursor()
            query = "SELECT Nombre_Cliente, Email_Cliente FROM Registro WHERE (Email_Cliente = %s OR Nombre_Cliente = %s) AND Rol_Usuario = 'cliente' "
            cursor.execute(query, (email, username))
            Is_Available = cursor.fetchone()

            print(Is_Available[0], Is_Available[1])

            if ((Is_Available[0] == username) and (Is_Available[1] == email)):

                flash("Email y nombre de usuario ya registrados. ")

            elif (Is_Available[0] == username):

                flash("Nombre de usuario ya registrado. ")

            elif (Is_Available[1] == email):

                flash("Email ya registrado. ")

            else:

                flash("Dev Log 001")

    else:

        type_Flash = "alert"
        redirect(url_for('login'))


    return render_template('login.html', type_Flash=type_Flash)

@app.route('/login', methods=['GET', 'POST'])
def login():

    type_Flash = "alert"

    if request.method == 'POST':

        print("Entra al POST. UWU ")
        email = request.form['email']
        password = request.form['pswd']
        role = request.form['role'] 

        cursor = db.cursor()
        query = "SELECT * FROM Registro WHERE Email_Cliente = %s AND Rol_Usuario = %s"
        cursor.execute(query, (email, role))
        user = cursor.fetchone()
        
        if user is not None:

            stored_hash = user[3]
            validacion = check_password_hash(stored_hash, password)
            print("Aca esta la validacion: ", validacion)

            if validacion:
            
                session['ID_Registro'] = user[0]
                session['User'] = user[1]
                session['Type_User'] = user[4]
                
                if user[4] == 'administrador':
                    
                    type_Flash = "alert-success"
                    return redirect(url_for('Admin_View'));
                
                else:
                    type_Flash = "alert-success"
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

@app.route('/about') 
def about():
        return render_template('about.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')

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
            
            type_Flash = "alert-danger"            
            flash("Email y Usuario no encontrados. ")
            
            print("Usuario No encontrado, verifique que el correo y contraseña sean validos. ")
            
        else:
            
            print("Si entra al else.  :D .")
            ID_User = user[0]
            
            cursor = db.cursor()
            query = "SELECT * FROM Reservas Where Cliente_ID_F = %s"
            cursor.execute(query, (ID_User,))
            user_reservation = cursor.fetchall()
            
            if user_reservation is None:
            
                cursor = db.cursor()
                query = "INSERT INTO Reservas (Cantidad_De_Sillas, Hora_Reserva, Fecha_Reserva, Cliente_ID_F) VALUES (%s, %s, %s, %s)"
                values = (Num_Personas_Reserva, Hora_Reserva, Fecha_Reserva, ID_User)
                cursor.execute(query, values)
                db.commit()
                
                type_Flash = "alert-success"
                flash('Reserva creada exitosamente!')
                
            else:
                
                type_Flash = "alert-danger"
                flash("El usuario ya realizo una reserva. ")
            
    else:
        
        type_Flash = "alert"
        
    return render_template('reservation.html', type_Flash=type_Flash)

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
def historia_1():
    return render_template('sabermas1.html')

@app.route('/vision')
def vision_1():
    return render_template('vision.html')

@app.route('/logout')
def logout():
    
    session.clear()
    
    print("Sesión eliminada")

    return redirect(url_for('login'))



@app.route('/admin_view')
def Admin_View():
    
    cursor = db.cursor()
    query = "SELECT * FROM Registro WHERE Rol_Usuario = 'cliente' "
    cursor.execute(query, )
    Listado_Users = cursor.fetchall()
    
    return render_template('Admin_Page_View.html', Listado_Usuarios = Listado_Users)

@app.route('/Editar_Usuario/<int:id>', methods = ['GET','POST'])
def Editar_Usuario(id):

    cursor = db.cursor()
    if request.method == 'POST':

        print("Esta entrando POST. ")
        Username = request.form ['txt']
        Email = request.form['Email']

        cursor = db.cursor()
        query = "SELECT Nombre_Cliente, Email_Cliente FROM Registro WHERE (Email_Cliente = %s OR Nombre_Cliente = %s) AND Rol_Usuario = 'cliente' And ID_Registro != %s"
        cursor.execute(query, (Email, Username, id))
        Is_Available = cursor.fetchone()

        if Is_Available is None:

            Update_Data = "UPDATE Registro set Nombre_Cliente = %s, Email_Cliente = %s Where ID_Registro = %s"
            cursor.execute(Update_Data,(Username, Email, id))
            db.commit()
            type_Flash = "alert-success"
            flash("Datos modificados exitosamente. ")

            return redirect(url_for('Admin_View'))

        else:

            type_Flash = "alert-danger"
            print(Is_Available[0], Is_Available[1])

            if ((Is_Available[0] == Username) and (Is_Available[1] == Email)):

                flash("Email y nombre de usuario ya registrados. ")

            elif (Is_Available[0] == Username):

                flash("Nombre de usuario ya registrado. ")

            elif (Is_Available[1] == Email):

                flash("Email ya registrado. ")

            else:

                flash("Dev Log 001")

    else:
        #obtener los datos de la persona que va a editar
        type_Flash = "alert"

        print("Esta llegando como GET. ")
        cursor = db.cursor()
        cursor.execute('SELECT * FROM registro WHERE ID_Registro = %s', (id,))
        data = cursor.fetchall()

        print(data)
    
    cursor = db.cursor()
    cursor.execute('SELECT * FROM registro WHERE ID_Registro = %s', (id,))
    data = cursor.fetchall()

    return render_template('Editar.html', data = data[0], type_Flash = type_Flash) 

@app.route('/Eliminar_Usuario/<int:id>', methods=['GET'])
def Eliminar_Usuario(id):
    
    cursor = db.cursor();
    cursor.execute('DELETE FROM Registro WHERE ID_Registro = %s', (id,))
    db.commit()
    return redirect(url_for('Admin_View'))

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

app.run(debug=True, port=5005)