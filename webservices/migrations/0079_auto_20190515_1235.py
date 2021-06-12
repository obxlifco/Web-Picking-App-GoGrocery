# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-15 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0078_engageboostvehiclemasters_vehicle_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboosttrentpicklists',
            name='is_sub_picklist',
            field=models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2),
        ),
        migrations.AddField(
            model_name='engageboosttrentpicklists',
            name='picklist_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]