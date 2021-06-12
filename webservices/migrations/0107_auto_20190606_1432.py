# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-06 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0106_engageboostgiftcardmasters'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostcustomerloyaltypoints',
            name='burn_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='engageboostcustomerloyaltypoints',
            name='card_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostcustomerloyaltypoints',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostcustomerloyaltypoints',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostcustomerloyaltypoints',
            name='valid_form',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcustomerloyaltypoints',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcustomerloyaltypoints',
            name='customer_contact_no',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcustomerloyaltypoints',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcustomerloyaltypoints',
            name='website_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
