# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-10 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0069_auto_20190510_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostordermaster',
            name='pos_device_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
