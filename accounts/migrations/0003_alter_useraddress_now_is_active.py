# Generated by Django 4.1 on 2022-10-18 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_is_active_useraddress_now_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='now_is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]