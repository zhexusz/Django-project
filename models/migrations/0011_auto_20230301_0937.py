# Generated by Django 3.2.18 on 2023-03-01 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_alter_userinfo_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlikes',
            name='blogId',
        ),
        migrations.RemoveField(
            model_name='userlikes',
            name='selfIntroduction',
        ),
        migrations.RemoveField(
            model_name='userlikes',
            name='userStatus',
        ),
    ]
