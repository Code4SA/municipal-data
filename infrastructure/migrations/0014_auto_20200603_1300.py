# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-03 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0013_auto_20200602_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectquarterlyspend',
            name='q1',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='projectquarterlyspend',
            name='q2',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='projectquarterlyspend',
            name='q3',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='projectquarterlyspend',
            name='q4',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]
