# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-01 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0146_auto_20190731_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostorderproducts',
            name='substitute_product_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
