# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-30 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0096_engageboostwarehousesuppliermappings'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostwarehousesuppliermappings',
            name='website_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]