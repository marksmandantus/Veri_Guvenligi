
from django.core.files.base import ContentFile
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from .models import UploadedFile

def handle_uploaded_file(file, algorithm, key, user_profile, directory):
    if algorithm == 'none':
        # Şifreleme yapma
        new_uploaded_file = UploadedFile()
        new_uploaded_file.user_profile = user_profile
        new_uploaded_file.directory = directory
        new_uploaded_file.file = file
        new_uploaded_file.save()
    else:
        # Şifreleme yap
        encrypted_data = encrypt_file(file.read(), algorithm, key)

        new_uploaded_file = UploadedFile()
        new_uploaded_file.user_profile = user_profile
        new_uploaded_file.directory = directory
        new_uploaded_file.file.save(file.name, ContentFile(encrypted_data))
        new_uploaded_file.save()
