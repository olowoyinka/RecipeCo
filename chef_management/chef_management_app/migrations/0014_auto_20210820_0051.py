# Generated by Django 3.2.5 on 2021-08-19 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_management_app', '0013_auto_20210819_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='message',
            field=models.CharField(default='declined', max_length=255),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='booking_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='booking_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]