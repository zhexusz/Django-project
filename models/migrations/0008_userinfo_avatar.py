# Generated by Django 3.2.18 on 2023-03-01 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_userlogin_expiretime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/avatars/'),
        ),
    ]
