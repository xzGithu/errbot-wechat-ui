# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-31 01:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0013_auto_20181031_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qunper',
            old_name='rulename',
            new_name='qunrulename',
        ),
    ]
