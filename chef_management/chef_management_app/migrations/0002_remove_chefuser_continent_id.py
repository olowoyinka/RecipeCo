# Generated by Django 3.2.5 on 2021-07-23 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chefuser',
            name='continent_id',
        ),
    ]