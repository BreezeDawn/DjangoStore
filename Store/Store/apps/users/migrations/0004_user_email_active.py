# Generated by Django 2.1.1 on 2018-09-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180922_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BooleanField(default=False, verbose_name='邮箱验证状态'),
        ),
    ]
