# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-24 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0123_engageboostpages_template_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostdiscountmastersconditions',
            name='all_product_qty',
            field=models.TextField(blank=True, null=True),
        ),
        # migrations.AddField(
        #     model_name='engageboostpages',
        #     name='template_image',
        #     field=models.TextField(blank=True, null=True),
        # ),
    ]
