# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-25 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0014_auto_20200603_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
