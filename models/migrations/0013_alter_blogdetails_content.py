# Generated by Django 3.2.18 on 2023-03-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0012_blogdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdetails',
            name='content',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='content'),
        ),
    ]