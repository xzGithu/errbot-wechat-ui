# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-31 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0016_auto_20181031_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='SinPer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sinname', models.CharField(max_length=400, verbose_name='备注名')),
                ('Sinrulename', models.ManyToManyField(max_length=400, related_name='sinper', to='useraction.rulelistmodel', verbose_name='规则名称')),
            ],
        ),
    ]