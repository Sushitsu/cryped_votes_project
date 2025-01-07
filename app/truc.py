from flask import render_template, request, redirect, url_for, flash, session
from app import db

from app import app
from app.models import User

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
        elif len(password) < 8 or not any(char.isupper() for char in password) or not any(
                char.isdigit() for char in password):
            flash('Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule et un chiffre.', 'error')
        else:
            if User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur existe déjà.', 'error')
            else:
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  # Effacer toutes les données de session
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login'))  # Rediriger vers la page de connexion
