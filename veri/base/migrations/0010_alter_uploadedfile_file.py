# Generated by Django 4.2.3 on 2023-12-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_uploadedfile_encrypted_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='uploads'),
        ),
    ]
