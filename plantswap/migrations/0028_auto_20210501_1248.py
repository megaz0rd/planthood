# Generated by Django 3.0.6 on 2021-05-01 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plantswap', '0027_auto_20210501_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match', to='plantswap.Match'),
        ),
    ]