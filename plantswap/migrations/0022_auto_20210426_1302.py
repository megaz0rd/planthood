# Generated by Django 3.0.6 on 2021-04-26 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plantswap', '0021_message_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='plant',
        ),
        migrations.AddField(
            model_name='transaction',
            name='plant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plantswap.Match'),
            preserve_default=False,
        ),
    ]
