# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-11 14:42
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20190322_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interview_skills',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name=models.CharField()),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_interviewer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=25),
        ),
    ]
