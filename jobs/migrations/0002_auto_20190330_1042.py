# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-30 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_status_value',
            field=models.CharField(default='Active', max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='status_value',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_end_date',
            field=models.DateField(default='2019-05-14', null=True),
        ),
    ]
