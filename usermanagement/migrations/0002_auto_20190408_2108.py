# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-08 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_id', models.SmallIntegerField(null=True)),
                ('message', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='primary_user',
            field=models.BooleanField(default=False),
        ),
    ]
