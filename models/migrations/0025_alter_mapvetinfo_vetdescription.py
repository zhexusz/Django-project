# Generated by Django 3.2.18 on 2023-03-01 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0024_auto_20230301_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapvetinfo',
            name='vetDescription',
            field=models.CharField(default=None, max_length=2000, verbose_name='vetDescription'),
        ),
    ]