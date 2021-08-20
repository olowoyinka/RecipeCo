# Generated by Django 3.2.5 on 2021-08-20 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chef_management_app', '0014_auto_20210820_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='chefuser_id',
            field=models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.chefuser'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='message',
            field=models.CharField(default='Pending', max_length=255),
        ),
    ]
