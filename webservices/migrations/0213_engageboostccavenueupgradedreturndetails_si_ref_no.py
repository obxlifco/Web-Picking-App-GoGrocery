# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-08-11 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0212_auto_20200716_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostccavenueupgradedreturndetails',
            name='si_ref_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
