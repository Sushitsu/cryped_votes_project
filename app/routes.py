from flask import render_template, request, redirect, url_for, flash
from app import app

# Utilisateur fictif pour la démonstration
USERNAME = 'admin'
PASSWORD = 'password123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('home'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
