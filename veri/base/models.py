from django.contrib.auth.models import User
from django.db import models
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from django.core.files.base import ContentFile
import os 

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Directory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


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
            print("Encrypting using Blowfish algorithm...")

            cipher = Cipher(algorithms.Blowfish(key), modes.CFB8(), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            print("Encryption successful.")
            return ciphertext
        else:
            print("No encryption selected. Returning plaintext.")
            return plaintext

