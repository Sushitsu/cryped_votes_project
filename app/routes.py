from flask import render_template, request, redirect, url_for, flash

# Utilisateur fictif pour la démonstration
USERNAME = 'admin'
PASSWORD = 'password123'

def setup(app):
    # Page de login
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

    # Route de la page d'acceuil quand connecter
    @app.route('/home')
    def home():
        return render_template('home.html')

    # Route pour se déconnecter
    @app.route('/logout')
    def logout():
        # Logique de déconnexion, par exemple effacer la session
        return redirect(url_for('login'))