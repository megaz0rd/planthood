# Generated by Django 3.0.14 on 2021-05-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20210514_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='location',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='building_number',
            field=models.CharField(default=1, max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='street',
            field=models.CharField(default='Wiktorska', max_length=64),
            preserve_default=False,
        ),
    ]
