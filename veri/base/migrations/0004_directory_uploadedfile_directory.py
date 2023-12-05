# Generated by Django 4.2.3 on 2023-12-04 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_uploadedfile_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='directory',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='base.directory'),
            preserve_default=False,
        ),
    ]