# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-22 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0138_auto_20190717_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboosttaxsettings',
            name='shipping_tax_rate',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
