# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-06 13:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0014_auto_20170806_2255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infos',
            old_name='职职',
            new_name='职称',
        ),
    ]