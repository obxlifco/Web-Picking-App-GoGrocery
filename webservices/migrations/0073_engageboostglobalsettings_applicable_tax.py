# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-13 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0072_engageboostmultiplebarcodes_website_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostglobalsettings',
            name='applicable_tax',
            field=models.CharField(choices=[('GST', 'GST'), ('VAT', 'VAT')], max_length=10, null=True),
        ),
    ]