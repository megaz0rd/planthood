# Generated by Django 3.0.6 on 2021-05-01 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plantswap', '0028_auto_20210501_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='plantswap.Match'),
        ),
        migrations.AlterField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]
