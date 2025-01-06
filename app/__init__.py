from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Nécessaire pour utiliser flash

from app import routes  # Importe les routes
