# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-07 07:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0158_merge_20190806_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engageboostproductpricetypemaster',
            name='warehouse_id',
        ),
    ]