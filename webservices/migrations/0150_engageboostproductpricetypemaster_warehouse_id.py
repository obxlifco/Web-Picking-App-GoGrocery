# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-02 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0149_remove_engageboostproductpricetypemaster_warehouse_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostproductpricetypemaster',
            name='warehouse_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
