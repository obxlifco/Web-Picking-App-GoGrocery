# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-25 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0139_engageboosttaxsettings_shipping_tax_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engageboosttrafficreports',
            name='average_duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboosttrafficreportsbrowsers',
            name='average_duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboosttrafficreportsmobiles',
            name='average_duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboosttrafficreportspages',
            name='average_duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboosttrafficreportspages',
            name='pageviews',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboosttrafficreportssources',
            name='average_duration',
            field=models.FloatField(blank=True, null=True),
        ),
    ]