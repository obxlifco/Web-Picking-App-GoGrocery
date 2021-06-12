# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-01 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0182_engageboosttemporaryshoppingcarts_warehouse_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engageboostcountries',
            name='isblocked',
            field=models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2),
        ),
        migrations.AlterField(
            model_name='engageboostcountries',
            name='isdeleted',
            field=models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2),
        ),
        migrations.AlterField(
            model_name='engageboostrepricingmaximumminrules',
            name='isblocked',
            field=models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2),
        ),
        migrations.AlterField(
            model_name='engageboostrepricingmaximumminrules',
            name='isdeleted',
            field=models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2),
        ),
    ]