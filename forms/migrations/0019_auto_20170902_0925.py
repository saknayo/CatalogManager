# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-02 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0018_auto_20170901_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infos',
            name='上报时间',
            field=models.CharField(blank=True, default='', max_length=9),
        ),
        migrations.AlterField(
            model_name='infos',
            name='出生年月',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='infos',
            name='类别编号',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
