# Generated by Django 3.0.6 on 2021-04-16 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plantswap', '0008_auto_20210416_1847'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TransactionPlant',
            new_name='WantedPlant',
        ),
    ]
