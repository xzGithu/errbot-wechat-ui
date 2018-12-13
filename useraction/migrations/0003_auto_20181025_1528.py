# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-25 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0002_auto_20181023_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commands',
            name='rulename',
            field=models.CharField(max_length=400, verbose_name='规则名称'),
        ),
        migrations.AlterField(
            model_name='commands',
            name='status',
            field=models.CharField(choices=[('0', '启用'), ('1', '禁用')], max_length=50, verbose_name='状态'),
        ),
    ]
