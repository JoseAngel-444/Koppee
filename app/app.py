from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector, base64
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="koppa"
)


@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/about') 
def about():
    return render_template('about.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')


@app.route('/servicio')
def servicio():
    return render_template('service.html')



app.run(debug=True, port=5005)