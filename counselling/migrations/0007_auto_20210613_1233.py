# Generated by Django 3.1.4 on 2021-06-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselling', '0006_auto_20210613_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='time',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
