# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-07-16 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0211_engageboostalluserdevicetoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostSmsLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('sms_subject', models.CharField(blank=True, max_length=256, null=True)),
                ('sms_content_text', models.TextField(blank=True, null=True)),
                ('response_code', models.CharField(blank=True, max_length=50, null=True)),
                ('response_text', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'enageboost_sms_log',
            },
        ),
        migrations.DeleteModel(
            name='EngageboostAllUserDeviceToken',
        ),
    ]
