# Generated by Django 3.0.6 on 2021-04-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantswap', '0003_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='plants/'),
        ),
    ]