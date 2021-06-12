# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-21 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0120_auto_20190620_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostCustomFieldMastersLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.IntegerField(blank=True, null=True)),
                ('language_code', models.CharField(blank=True, max_length=20, null=True)),
                ('field_id', models.IntegerField(blank=True, null=True)),
                ('field_name', models.CharField(blank=True, max_length=100, null=True)),
                ('field_value', models.TextField(blank=True, null=True)),
                ('field_lable_value', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
            ],
            options={
                'db_table': 'engageboost_customfield_masters_lang',
            },
        ),
    ]