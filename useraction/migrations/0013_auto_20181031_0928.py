# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-31 01:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0012_qunper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qunper',
            name='rulename',
            field=models.ForeignKey(max_length=400, on_delete=django.db.models.deletion.CASCADE, related_name='rusper', to='useraction.rulelistmodel', verbose_name='规则名称'),
        ),
    ]
