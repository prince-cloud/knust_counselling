# Generated by Django 3.1.5 on 2021-06-11 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210611_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_counselor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]