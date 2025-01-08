from cryptography.fernet import Fernet 

# Générer une clé Fernet valide
key = Fernet.generate_key()  # Générer une clé

# Sauvegarder la clé dans un fichier sécurisé 
with open('app/secret.key', 'wb') as key_file:  
    key_file.write(key)  # Écrire la clé dans le fichier
 
print("Clé Fernet générée et sauvegardée dans 'secret.key'") 
