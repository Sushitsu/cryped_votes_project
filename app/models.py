from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash le mot de passe avant de le stocker."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe correspond au hash."""
        return check_password_hash(self.password_hash, password)
