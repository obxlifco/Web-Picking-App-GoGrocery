# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-15 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0140_remove_engageboostwarehousemanager_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostwarehousemanager',
            name='role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
