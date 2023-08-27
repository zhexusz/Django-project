# Generated by Django 3.2.18 on 2023-03-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0030_delete_blogimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogImages',
            fields=[
                ('imageId', models.AutoField(primary_key=True, serialize=False, verbose_name='imageId')),
                ('blogId', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='blogId')),
                ('imageUrls', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='imageUrls')),
            ],
            options={
                'db_table': 'blog_images',
            },
        ),
    ]