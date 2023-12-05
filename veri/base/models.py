from django.contrib.auth.models import User
from django.db import models

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