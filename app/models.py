from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import datetime
from app import db

# Chargement de la clé de chiffrement
def load_key():
    return open("app/secret.key", "rb").read()

# Initialisation de Fernet avec la clé
key = load_key()
cipher_suite = Fernet(key)

class User(db.Model):
    __tablename__ = 'user'  # Spécifie que le modèle correspond à la table 'users'
    
    # Définit 'username' comme clé primaire
    username = db.Column(db.String(64), primary_key=True, unique=True, nullable=False) # Ajout de la colonne 'username'
    password_hash = db.Column(db.String(64), nullable=False) # Ajout de la colonne 'password'
    secu = db.Column(db.String(13), nullable=False) # Ajout de la colonne 'secu'
    vote = db.Column(db.Boolean, default=False) # Ajout de la colonne 'vote'
    vote_time = db.Column(db.DateTime, nullable=True)   # Ajout de la colonne 'vote_time'
    admin = db.Column(db.Boolean, default=False) # Ajout de la colonne 'admin'
    
    def __repr__(self): 
        return f'<User {self.username}>'

    def set_password(self, password_hash):
        self.password_hash = cipher_suite.encrypt(password_hash.encode()).decode()

    def check_password(self, password_hash):
        return cipher_suite.decrypt(self.password_hash.encode()).decode() == password_hash

    def set_secu(self, secu):
        self.secu = cipher_suite.encrypt(secu.encode()).decode()

    def check_secu(self, secu):
        return cipher_suite.decrypt(self.secu.encode()).decode() == secu

    def register_vote(self):
        self.vote = True
        self.vote_time = datetime.datetime.now()  # Enregistrement du moment du vote
        db.session.commit() 

    def set_admin(self, admin_status): 
        self.admin = admin_status 
        db.session.commit() 
