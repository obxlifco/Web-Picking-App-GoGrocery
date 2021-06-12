# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-10-22 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0216_auto_20200925_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostordermaster',
            name='order_net_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostwarehousemasters',
            name='expected_delivery_time',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
