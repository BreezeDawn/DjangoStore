# Generated by Django 2.1.1 on 2018-09-22 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180920_1717'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='st_users',
        ),
    ]
