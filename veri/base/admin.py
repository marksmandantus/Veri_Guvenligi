from django.contrib import admin
from .models import UploadedFile, Directory

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'directory', 'file', 'uploaded_at', 'is_encrypted')

    
admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(Directory)
