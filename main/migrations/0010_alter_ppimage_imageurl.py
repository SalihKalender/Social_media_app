# Generated by Django 3.2.9 on 2022-06-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_ppimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppimage',
            name='imageURL',
            field=models.ImageField(default='', upload_to='profile_images'),
        ),
    ]