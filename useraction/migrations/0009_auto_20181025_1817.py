# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-25 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0008_auto_20181025_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commands',
            name='rulename',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='useraction.rulelistmodel', verbose_name='规则名称'),
        ),
    ]
