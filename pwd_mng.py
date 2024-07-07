import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json

# Constants
PASSWORD_FILE = "passwords.json"
SALT = os.urandom(16)  # Ideally, you would store this safely and not regenerate it each run

# Derive key from a password
def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 key length is 32 bytes
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt a message
def encrypt(message: str, key: bytes) -> str:
    iv = os.urandom(12)  # Generate a random IV
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return urlsafe_b64encode(iv + encryptor.tag + ciphertext).decode()

# Decrypt a message
def decrypt(token: str, key: bytes) -> str:
    token_bytes = urlsafe_b64decode(token.encode())
    iv = token_bytes[:12]
    tag = token_bytes[12:28]
    ciphertext = token_bytes[28:]

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()

# Save passwords to a file
def save_passwords(passwords: dict, key: bytes):
    encrypted_passwords = {k: encrypt(v, key) for k, v in passwords.items()}
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(encrypted_passwords, file)

# Load passwords from a file
def load_passwords(key: bytes) -> dict:
    if not os.path.exists(PASSWORD_FILE):
        return {}
    
    with open(PASSWORD_FILE, 'r') as file:
        encrypted_passwords = json.load(file)

    return {k: decrypt(v, key) for k, v in encrypted_passwords.items()}

# Main password manager logic
def main():
    master_password = input("Enter your master password: ")
    key = derive_key(master_password, SALT)
    
    passwords = load_passwords(key)
    
    while True:
        action = input("Choose an action: [add/list/exit] ").lower()
        os.system('cls')
        if action == 'add':
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            passwords[service] = password
            save_passwords(passwords, key)
            print(f"Password for {service} added.")
        
        elif action == 'list':
            for service, password in passwords.items():
                print(f"Service: {service}, Password: {password}")
        
        elif action == 'exit':
            break
        
        else:
            print("Invalid action. Please choose [add/list/exit].")

if __name__ == "__main__":
    main()
