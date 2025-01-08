import rsa

# Générer une clé RSA de 512 bits
def generate_rsa_keys():
    public_key, private_key = rsa.newkeys(512)  # Générer des clés RSA de 512 bits
    return private_key, public_key

# Exemple d'utilisation
private_key, public_key = generate_rsa_keys()

# Affichage des clés générées
print("Clé privée:", private_key.save_pkcs1().decode())
print("Clé publique:", public_key.save_pkcs1().decode())

# Vous pouvez également démontrer la vulnérabilité en essayant de casser la clé.