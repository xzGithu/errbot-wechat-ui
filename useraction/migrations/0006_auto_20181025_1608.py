# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-25 08:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0005_auto_20181025_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rulelistmodel',
            name='fanan',
        ),
        migrations.RemoveField(
            model_name='rulelistmodel',
            name='params',
        ),
        migrations.RemoveField(
            model_name='rulelistmodel',
            name='status',
        ),
        migrations.RemoveField(
            model_name='rulelistmodel',
            name='zhiling',
        ),
    ]
