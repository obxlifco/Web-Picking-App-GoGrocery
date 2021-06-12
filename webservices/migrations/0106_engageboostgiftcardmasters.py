# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-06 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0105_remove_engageboostwarehousesuppliermappings_base_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostGiftCardMasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(blank=True, max_length=100, null=True)),
                ('card_name', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('createdby', models.IntegerField(blank=True, null=True)),
                ('modifiedby', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
            ],
            options={
                'db_table': 'engageboost_gift_card_masters',
            },
        ),
    ]