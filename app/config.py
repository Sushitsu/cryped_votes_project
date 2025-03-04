import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_clé_secrète'  # Remplace par ta clé secrète si nécessaire
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications pour économiser des ressources
    # Remplace les valeurs ci-dessous avec tes informations de connexion
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://votes:eu[KNAUL-nQL8WHU@kyosu.fr/votes_system'
    )
    # Utilise "vote" comme utilisateur, "your_password" comme mot de passe et "votes_system" comme nom de base
