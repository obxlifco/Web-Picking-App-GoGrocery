# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-23 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0191_auto_20191022_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engageboostordermaster',
            name='mobiquest_passcode',
        ),
        migrations.RemoveField(
            model_name='engageboostordermaster',
            name='mobiquest_point_discount',
        ),
        migrations.AddField(
            model_name='engageboostordermaster',
            name='pay_wallet_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='engageboostordermaster',
            name='refund_wallet_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]