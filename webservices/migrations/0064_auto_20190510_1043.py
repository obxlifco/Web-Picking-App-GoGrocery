# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-10 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0063_merge_20190510_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostrolemasters',
            name='website_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='access_key',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='website_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]