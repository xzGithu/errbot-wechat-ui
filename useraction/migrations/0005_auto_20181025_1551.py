# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-25 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0004_auto_20181025_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commands',
            name='rulename',
        ),
        migrations.AddField(
            model_name='rulelistmodel',
            name='fanan',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='方案名称'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rulelistmodel',
            name='params',
            field=models.CharField(default=django.utils.timezone.now, max_length=300, verbose_name='参数顺序'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rulelistmodel',
            name='status',
            field=models.CharField(choices=[('0', '启用'), ('1', '禁用')], default=1, max_length=50, verbose_name='状态'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rulelistmodel',
            name='zhiling',
            field=models.CharField(default=2, max_length=400, verbose_name='指令用例'),
            preserve_default=False,
        ),
    ]