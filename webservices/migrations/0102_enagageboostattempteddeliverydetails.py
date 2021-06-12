# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-03 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0101_merge_20190603_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnagageboostAttemptedDeliveryDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_id', models.IntegerField(blank=True, null=True)),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('delivery_attempted_date', models.DateTimeField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('additional_note', models.TextField(blank=True, null=True)),
                ('new_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('attempted_type', models.CharField(blank=True, choices=[('attempt', 'attempt'), ('delivered', 'delivered')], max_length=20, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
            ],
            options={
                'db_table': 'enagageboost_attempted_delivery_details',
            },
        ),
    ]
