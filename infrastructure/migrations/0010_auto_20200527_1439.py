# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-05-27 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0009_content_search_triggers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectQuarterlySpend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.DecimalField(decimal_places=2, max_digits=20)),
                ('q2', models.DecimalField(decimal_places=2, max_digits=20)),
                ('q3', models.DecimalField(decimal_places=2, max_digits=20)),
                ('q4', models.DecimalField(decimal_places=2, max_digits=20)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infrastructure.FinancialYear')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarterly', to='infrastructure.Project')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='projectquarterlyspend',
            unique_together=set([('project', 'financial_year')]),
        ),
    ]
