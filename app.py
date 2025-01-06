from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3  # Pour interagir avec SQLite

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_PATH = 'test.db'  # Chemin de la base de données SQLite

# Route principale
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validation fictive
        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

# Route pour afficher les utilisateurs
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Récupérer les utilisateurs
    cursor.execute('SELECT id, name, email, public_key, created_at FROM users')
    users = cursor.fetchall()

    # Fermer la connexion
    conn.close()

    # Passer les utilisateurs au template
    return render_template('home.html', users=users)

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)