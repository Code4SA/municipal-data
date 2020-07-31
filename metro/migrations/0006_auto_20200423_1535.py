# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-04-23 13:35
from __future__ import unicode_literals

from django.db import migrations


def remove_empty_elements(apps, schema_editor):
    Element = apps.get_model("metro", "IndicatorElements")
    for element in Element.objects.all():
        if element.name == "":
            element.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("metro", "0005_auto_20200423_1515"),
    ]

    operations = [migrations.RunPython(remove_empty_elements)]
