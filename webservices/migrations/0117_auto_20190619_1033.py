# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-19 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0116_merge_20190619_0757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engageboostinvoicemaster',
            name='created_date',
        ),
        migrations.AddField(
            model_name='engageboostinvoicemaster',
            name='created',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engageboostinvoicemaster',
            name='modified',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostinvoicemaster',
            name='shipment_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='engageboostinvoicemaster',
            name='trent_picklist_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]