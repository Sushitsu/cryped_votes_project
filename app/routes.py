from flask import render_template, request, redirect, url_for, flash, session

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
