# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 13:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0012_auto_20170804_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historys',
            name='edit_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
