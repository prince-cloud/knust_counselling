# Generated by Django 3.1.4 on 2021-06-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210611_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='counsellor',
            name='bio',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_nuumber',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default=1, upload_to='profile_pictures/'),
            preserve_default=False,
        ),
    ]