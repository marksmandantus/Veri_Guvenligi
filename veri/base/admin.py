from django.contrib import admin
from .models import UploadedFile, Directory

admin.site.register(UploadedFile)
admin.site.register(Directory)
