# Generated by Django 3.2.18 on 2023-03-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0026_userlikes_userbeenlikedid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, default='/', max_length=255, null=True, upload_to='images/avatars/'),
        ),
    ]