# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-04 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0043_merge_20190404_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostordermaster',
            name='order_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcreditpointconditions',
            name='loyalty_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CreditPointConditions', to='webservices.EngageboostCreditPoint'),
        ),
        migrations.AlterField(
            model_name='engageboostproductstocks',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_stock', to='webservices.EngageboostProducts'),
        ),
    ]