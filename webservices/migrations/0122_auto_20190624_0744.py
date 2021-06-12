# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-24 07:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0121_engageboostdiscountmasters_warehouse_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostDiscountFreebieMappings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('isdeleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('isblocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('createdby', models.IntegerField(blank=True, null=True)),
                ('updatedby', models.IntegerField(blank=True, null=True)),
                ('discount_master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DiscountFreebieMappings', to='webservices.EngageboostDiscountMasters')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DiscountFreebieProducts', to='webservices.EngageboostProducts')),
            ],
            options={
                'db_table': 'engageboost_discount_freebie_mappings',
            },
        )#,
        # migrations.AddField(
        #     model_name='engageboostpages',
        #     name='template_image',
        #     field=models.TextField(blank=True, null=True),
        # ),
    ]