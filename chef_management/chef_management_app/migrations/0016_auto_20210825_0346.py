# Generated by Django 3.2.5 on 2021-08-25 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chef_management_app', '0015_auto_20210820_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='chefuser_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.chefuser'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.recipe'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_time', models.TimeField()),
                ('booking_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('message', models.CharField(default='Pending', max_length=255)),
                ('chefuser_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.chefuser')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.recipe')),
                ('regularuser_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_management_app.regularuser')),
            ],
        ),
    ]
