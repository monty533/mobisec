# Generated by Django 4.2.3 on 2023-07-23 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
