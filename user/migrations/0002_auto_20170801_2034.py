# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='url',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]