# Generated by Django 3.2.18 on 2023-03-01 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_alter_userinfo_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, default='/', null=True, upload_to='images/avatars/'),
        ),
    ]
