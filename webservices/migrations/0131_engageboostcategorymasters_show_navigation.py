# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-04 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0130_auto_20190704_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostcategorymasters',
            name='show_navigation',
            field=models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True),
        ),
    ]