# Generated by Django 3.1.4 on 2021-08-01 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210617_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='counsellor',
            name='office_number',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]