# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-25 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0053_auto_20190424_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostordermaster',
            name='pay_txndate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
