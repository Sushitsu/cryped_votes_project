from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # nécessaire pour utiliser flash

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
    return "Bienvenue sur la page d'accueil !"

if __name__ == '__main__':
    app.run(debug=True)
