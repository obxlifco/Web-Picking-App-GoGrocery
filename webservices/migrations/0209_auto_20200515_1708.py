# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-15 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0208_auto_20200327_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostshippingmasterssettings',
            name='picking_type',
            field=models.CharField(choices=[('HomeDelivery', 'HomeDelivery'), ('SelfPickup', 'SelfPickup')], default='HomeDelivery', max_length=20),
        ),
        migrations.AddField(
            model_name='engageboostshippingmasterssettings',
            name='self_pickup_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='engageboostshippingmasterssettings',
            name='zone_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostshipmentorders',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipment_order', to='webservices.EngageboostOrdermaster'),
        ),
    ]
