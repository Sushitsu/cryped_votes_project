from flask import render_template, request, redirect, url_for, flash, session
from app.models import User
from app import db


# Utilisateur fictif pour la démonstration
USERNAME = 'admin'
PASSWORD = 'password123'

# Liste des candidats fictifs
CANDIDATS = ['Candidat 1', 'Candidat 2', 'Candidat 3']

def setup(app):
    
    # Page de login
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if username == USERNAME and password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
        
        return render_template('login.html')

    # Route de la page d'accueil (connecté)
    @app.route('/home')
    def home():
        if not session.get('logged_in'):  # Vérifie si l'utilisateur est connecté
            return redirect(url_for('login'))
        
        return render_template('home.html', candidats=CANDIDATS)

# Route pour l'inscription d'un nouvel utilisateur
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            secu = request.form['secu']  # Numéro de sécurité sociale
            vote = False  # L'utilisateur n'a pas encore voté
            vote_time = None  # Pas de vote au début
            admin = 0  # Définit l'utilisateur comme non admin (admin=0)

            # Validation des mots de passe
            if password != confirm_password:
                flash('Les mots de passe ne correspondent pas.', 'error')
            elif len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
                flash('Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule et un chiffre.', 'error')
            else:
                # Vérifier si l'utilisateur existe déjà
                if User.query.filter_by(username=username).first():
                    flash('Ce nom d\'utilisateur existe déjà.', 'error')
                else:
                    # Créer un nouvel utilisateur avec tous les champs nécessaires
                    new_user = User(
                        username=username,
                        vote=vote,
                        vote_time=vote_time,
                        admin=admin  # L'utilisateur est un utilisateur classique, donc admin=0
                    )
                    # Utiliser les méthodes du modèle pour configurer le mot de passe et le numéro de sécu
                    new_user.set_password(password)
                    new_user.set_secu(secu)

                    # Ajouter l'utilisateur à la base de données
                    db.session.add(new_user)
                    db.session.commit()

                    flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
                    return redirect(url_for('login'))

        return render_template('register.html')


    # Route pour enregistrer un vote
    @app.route('/vote', methods=['POST'])
    def vote():
        candidat = request.form.get('candidat')
        
        if not candidat or candidat not in CANDIDATS:
            flash('Vote invalide.', 'error')
            return redirect(url_for('home'))
        
        # Logique d'enregistrement du vote (ajouter dans une base ou stocker temporairement)
        flash(f"Votre vote pour {candidat} a été enregistré !", 'success')
        return redirect(url_for('home'))

    # Route pour se déconnecter
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)  # Déconnecte l'utilisateur
        flash('Vous avez été déconnecté.', 'info')
        return redirect(url_for('login'))
