from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hmac, hashlib

# Générer une clé RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Générer une clé AES
def generate_aes_key():
    return get_random_bytes(32)  # 256 bits

# Chiffrer un message avec AES
def encrypt_aes(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    return cipher.iv, ciphertext

# Déchiffrer un message avec AES
def decrypt_aes(iv, ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

# Chiffrer la clé AES avec RSA
def encrypt_rsa(aes_key, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.encrypt(aes_key)

# Déchiffrer la clé AES avec RSA
def decrypt_rsa(encrypted_key, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.decrypt(encrypted_key)

# Générer un HMAC pour vérifier l’intégrité
def generate_hmac(message, key):
    return hmac.new(key, message, hashlib.sha256).hexdigest()
