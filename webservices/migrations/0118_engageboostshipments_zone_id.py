# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-20 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0117_auto_20190619_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostshipments',
            name='zone_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
