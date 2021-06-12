# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-28 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0031_auto_20190228_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engageboostgridcolumnlayouts',
            name='isblocked',
            field=models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostgridcolumnlayouts',
            name='isdeleted',
            field=models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostgridlayouts',
            name='isblocked',
            field=models.CharField(blank=True, choices=[('n', 'n'), ('y', 'y')], default='n', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostgridlayouts',
            name='isdeleted',
            field=models.CharField(blank=True, choices=[('n', 'n'), ('y', 'y')], default='n', max_length=2, null=True),
        ),
    ]