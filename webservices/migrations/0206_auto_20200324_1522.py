# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-03-24 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0205_auto_20200319_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engageboostcategorybanners',
            name='warehouse',
        ),
        migrations.AddField(
            model_name='engageboostcategorybanners',
            name='warehouse_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
