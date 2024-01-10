from django.contrib.auth.models import User
from django.db import models
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os 
from os import urandom
from cryptography.hazmat.primitives import padding
from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Directory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def rc4_encrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def write_key_to_file(key, algorithm):
    keys_folder = 'keys'
    key_file_path = os.path.join(keys_folder, f'{algorithm}_key.txt')

    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder)

    with open(key_file_path, 'a') as key_file:
        key_file.write(key + os.linesep)

def encrypt_key_folder_with_rc4(key_folder_path, rc4_key):
    if not os.path.exists(key_folder_path):
        os.makedirs(key_folder_path)

    for filename in os.listdir(key_folder_path):
        file_path = os.path.join(key_folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as key_file:
                key_data = key_file.read()
            
            encrypted_data = rc4_encrypt(key_data, rc4_key)

            with open(file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

def pad(data):
    padder = padding.PKCS7(64).padder()  # 64 is the block size in bits (8 bytes)
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encryption_algorithm = models.CharField(max_length=255, null=True, blank=True)
    encryption_key = models.CharField(max_length=255, null=True, blank=True)
    encrypted_file = models.BinaryField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    

    def encrypt_file(self, plaintext, algorithm, key):
        print(f"Algorithm: {algorithm}, Key: {key}")

        write_key_to_file(key, algorithm)

        if algorithm == 'des':
            print(f"Plaintext: {plaintext}, Key: {key}")

            key = key.ljust(8)[:8].encode()  # DES anahtarı 8 byte olmalı
            iv = b'01234567'
            print("Encrypting using DES algorithm...")

            # file deepcode ignore InsecureCipher: <DES algoritması güvenli değil!>
            cipher = Cipher(algorithms.TripleDES(key), modes.CFB8(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            print("Encryption successful.")
            return ciphertext
        
        elif algorithm == 'aes':
            print(f"Plaintext: {plaintext}, Key: {key}")

            kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,  # 32 bytes = 256 bits
            salt=os.urandom(16),
            iterations=100000,  # You can adjust the number of iterations based on your security requirements
            backend=default_backend())
            key = kdf.derive(key.encode())
            iv = os.urandom(16)  # Rastgele IV oluşturma
            print("Encrypting using AES algorithm...")

            cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            print("Encryption successful.")
            return ciphertext
        elif algorithm == 'blowfish':
            print(f"Plaintext: {plaintext}, Key: {key}")

            key = key.ljust(16)[:16].encode()  # Anahtarı kodlama işlemi ve uzunluğu 16 byte'a tamamlama
            iv = urandom(8)  # Generate a random 8-byte initialization vector

            print("Encrypting using Blowfish algorithm...")

            padded_plaintext = pad(plaintext)

            cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

            print("Encryption successful.")
            return ciphertext
        else:
            print("No encryption selected. Returning plaintext.")
            return plaintext
        
rc4_key = get_random_bytes(16)
key_folder_path = 'keys'
encrypt_key_folder_with_rc4(key_folder_path, rc4_key)

