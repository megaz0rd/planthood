# Generated by Django 3.0.6 on 2021-04-16 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantswap', '0010_auto_20210416_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='plant',
        ),
        migrations.AddField(
            model_name='transaction',
            name='plant',
            field=models.ManyToManyField(to='plantswap.WantedPlant'),
        ),
    ]