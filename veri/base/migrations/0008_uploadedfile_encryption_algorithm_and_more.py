# Generated by Django 4.2.3 on 2023-12-09 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_directory_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='encryption_algorithm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='encryption_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
