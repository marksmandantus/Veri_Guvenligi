from django.contrib.auth.models import User
from django.db import models
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from django.core.files.base import ContentFile

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

    def encrypt_file(self, plaintext, algorithm, key):
        if algorithm == 'des':
            pass
        elif algorithm == 'aes':
            key = base64.b64decode(key.encode())
            cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            return base64.b64encode(ciphertext).decode()
        elif algorithm == 'blowfish':
            pass
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
