# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-15 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0142_remove_engageboostcategorymasters_show_navigation'),
    ]

    operations = [
        migrations.AddField(
            model_name='engageboostcategorymasters',
            name='show_navigation',
            field=models.CharField(blank=True, choices=[('Y', 'Y'), ('N', 'N')], default='N', max_length=2, null=True),
        ),
    ]