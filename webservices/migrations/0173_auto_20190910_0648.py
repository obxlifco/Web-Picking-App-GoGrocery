# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-10 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0172_engageboosttempproductprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engageboostcustomers',
            name='auth_user',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='webservices.EngageboostUsers'),
        ),
    ]
