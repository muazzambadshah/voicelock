# encryptor.py

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# --- Key Derivation from Password ---
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# --- Encrypt File ---
def encrypt_file(file_path: str, password: str):
    with open(file_path, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(file_path + '.enc', 'wb') as f:
        f.write(salt + encrypted)

    print(f"[✓] Encrypted -> {file_path}.enc")

# --- Decrypt File ---
def decrypt_file(enc_path: str, password: str, output_path: str = None):
    with open(enc_path, 'rb') as f:
        content = f.read()

    salt = content[:16]
    encrypted = content[16:]
    key = derive_key(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)

    output = output_path or enc_path.replace('.enc', '.wav')
    with open(output, 'wb') as f:
        f.write(decrypted)

    print(f"[✓] Decrypted -> {output}")

# --- CLI Test ---
if __name__ == "__main__":
    print("1. Encrypt\n2. Decrypt")
    choice = input("Select an option: ")

    if choice == "1":
        file = input("Enter path to file to encrypt: ")
        password = input("Enter password: ")
        encrypt_file(file, password)
    elif choice == "2":
        enc_file = input("Enter path to encrypted file (.enc): ")
        password = input("Enter password: ")
        decrypt_file(enc_file, password)
    else:
        print("Invalid option.")
