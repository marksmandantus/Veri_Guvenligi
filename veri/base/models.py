from django.contrib.auth.models import User
from django.db import models
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os 
from os import urandom
from cryptography.hazmat.primitives import padding

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Directory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

            key = key.encode()  # Anahtarı kodlama işlemi
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

            def pad(data):
                padder = padding.PKCS7(64).padder()  # 64 is the block size in bits (8 bytes)
                padded_data = padder.update(data) + padder.finalize()
                return padded_data

            padded_plaintext = pad(plaintext)

            cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

            print("Encryption successful.")
            return ciphertext
        else:
            print("No encryption selected. Returning plaintext.")
            return plaintext
        
    

