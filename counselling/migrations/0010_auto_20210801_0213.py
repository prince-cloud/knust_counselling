# Generated by Django 3.1.4 on 2021-08-01 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselling', '0009_schedule_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counselling',
            options={'ordering': ('date_created',)},
        ),
        migrations.AddField(
            model_name='counselling',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
