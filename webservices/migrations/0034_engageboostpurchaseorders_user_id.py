# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-14 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0033_auto_20190228_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostpurchaseorders',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
