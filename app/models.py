from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import bcrypt
import datetime
from hashlib import sha1
from app import db

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    aes_key = db.Column(db.LargeBinary, nullable=True)
    secu = db.Column(db.String(256), nullable=False)
    vote = db.Column(db.String(256), default=None)
    vote_time = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Hachage du mot de passe
    def encrypt_password(self, password):
        # return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return sha1(password.encode()).hexdigest()

    def set_password(self, password):
        self.password_hash = self.encrypt_password(password)

    def check_password(self, password):
        # return bcrypt.checkpw(password.encode(), self.password_hash.encode())
        return self.encrypt_password(password) == self.password_hash

    # Chiffrement et déchiffrement des données sécurisées
    def set_secu(self, secu):
        cipher = DES.new(self.get_aes_key(), DES.MODE_ECB)
        padded_secu = self.pad_data(secu.encode())
        self.secu = cipher.encrypt(padded_secu).hex()

    def check_secu(self, secu):
        cipher = DES.new(self.get_aes_key(), DES.MODE_ECB)
        decrypted_secu = self.unpad_data(cipher.decrypt(bytes.fromhex(self.secu)))
        return decrypted_secu.decode() == secu

    # Enregistrement du vote
    def register_vote(self, vote):
        cipher = DES.new(self.get_aes_key(), DES.MODE_ECB)
        padded_vote = self.pad_data(vote.encode())
        self.vote = cipher.encrypt(padded_vote).hex()
        self.vote_time = datetime.datetime.now()
        db.session.commit()

    def get_vote(self):
        if self.vote:
            try:
                cipher = DES.new(self.get_aes_key(), DES.MODE_ECB)
                decrypted_vote = self.unpad_data(cipher.decrypt(bytes.fromhex(self.vote)))
                return decrypted_vote.decode(), self.vote_time
            except ValueError as e:
                print(f"Erreur de déchiffrement : {e}")
                return None, None
        return None, None

    def set_admin(self, admin_status):
        self.admin = admin_status
        db.session.commit()

    # Gestion de la clé DES chiffrée avec RSA
    def encrypt_rsa(self, aes_key, public_key):
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        return cipher.encrypt(aes_key)

    def decrypt_rsa(self, encrypted_key, private_key):
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        return cipher.decrypt(encrypted_key)

    def generate_key(self):
        aes_key = b"8bytekey"  # La clé DES doit faire exactement 8 octets
        with open("app/rsa.pem") as rsa_key_file:
            public_key = rsa_key_file.read()
            self.aes_key = self.encrypt_rsa(aes_key, public_key)

    def get_aes_key(self):
        with open("app/rsa.key") as rsa_key_file:
            private_key = rsa_key_file.read()
            return self.decrypt_rsa(self.aes_key, private_key)

    # Méthodes utilitaires pour le padding
    @staticmethod
    def pad_data(data, block_size=8):
        padding_length = block_size - len(data) % block_size
        return data + bytes([padding_length] * padding_length)

    @staticmethod
    def unpad_data(data):
        padding_length = data[-1]
        return data[:-padding_length]

class Candidats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)
    nb_votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.name}'
