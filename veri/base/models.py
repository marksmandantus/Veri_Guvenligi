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
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encryption_algorithm = models.CharField(max_length=255, null=True, blank=True)
    encryption_key = models.CharField(max_length=255, null=True, blank=True)
    encrypted_file = models.BinaryField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)

    def encrypt_file(self, plaintext, algorithm, key):
        if algorithm == 'des':
            key = key.ljust(8)[:8].encode()  # DES anahtarı 8 byte olmalı
            iv = b'01234567'
            cipher = Cipher(algorithms.TripleDES(key), modes.CFB8(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            return base64.b64encode(ciphertext)
        if algorithm == 'aes':
            # Anahtarı base64 kod çözme işlemi yapmadan kullan
            key = key.encode()

            # CFB8 modu için uygun boyutta rastgele bir IV oluştur
            iv = os.urandom(16)

            # Şifreleme işlemi için Cipher objesini oluşturma
            cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())

            # Şifreleme işlemini gerçekleştirme
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            # IV'yi şifreli veriyle birleştirip base64 kodlama işlemi
            encrypted_data = base64.b64encode(iv + ciphertext)

            return encrypted_data
        elif algorithm == 'blowfish':
            key = key.ljust(16)[:16].encode()  # Blowfish anahtarı 16 byte olmalı
            cipher = Cipher(algorithms.Blowfish(key), modes.CFB8(), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            return base64.b64encode(ciphertext)
        else:
            # Şifreleme yapılmayacaksa direkt olarak plaintext'i döndür
            return plaintext


    def save(self, *args, **kwargs):
        if self.encryption_algorithm != 'none' and self.encryption_key:
            # Call save on the parent class (superclass) to save the file with the original name
            super().save(*args, **kwargs)

            # Read the original file content
            with open(self.file.path, 'rb') as file:
                plaintext = file.read()

            # Encrypt the content
            encrypted_text = self.encrypt_file(plaintext, self.encryption_algorithm, self.encryption_key)

            # Update the file name for encryption purposes
            self.file.name = 'uploads/' + self.file.name

            # Save the encrypted content to the file
            self.file.save(self.file.name, ContentFile(encrypted_text), save=False)

            # Call save again to save the model with the modified file name
            super().save(*args, **kwargs)
        else:
            # If encryption_algorithm or encryption_key is missing, save as usual
            super().save(*args, **kwargs)
