# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-11 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0173_auto_20190910_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostcustomers',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='engageboostcustomersaddressbook',
            name='billing_street_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostcustomersaddressbook',
            name='delivery_street_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]