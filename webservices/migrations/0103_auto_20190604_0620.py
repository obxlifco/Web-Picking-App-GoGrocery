# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-04 06:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0102_enagageboostattempteddeliverydetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engageboosttrentpicklists',
            name='delivery_date',
        ),
        migrations.RemoveField(
            model_name='engageboosttrentpicklists',
            name='invoice_date',
        ),
        migrations.RemoveField(
            model_name='engageboosttrentpicklists',
            name='invoice_id',
        ),
    ]
