# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-06 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0013_auto_20170804_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='infos',
            name='介绍人姓名',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='党校结业时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='入党志愿书编号',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='公示时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='函调时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='发展对象培训班',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='学位',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='导师',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='导师意见时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='工作时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='推优时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='支部书记',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='支部讨论入党时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='支部讨论转正时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='文化程度',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='申请书时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='确认入党积极分子的时间',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='职务',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='职职',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='infos',
            name='获奖情况',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='infos',
            name='民族',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='infos',
            name='籍贯',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='infos',
            name='职级',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='infos',
            name='身份证号',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
