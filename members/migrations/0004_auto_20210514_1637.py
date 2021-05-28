# Generated by Django 3.0.14 on 2021-05-14 14:37

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20210514_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(52.2036, 21.0002), geography=True, srid=4326),
        ),
    ]