# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-12 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0165_auto_20190812_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostCategoryBannersImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('banner_link_to', models.CharField(choices=[('external link', 'external link'), ('promotion', 'promotion'), ('category', 'category'), ('product', 'product')], default='category', max_length=20)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('promotion_id', models.IntegerField(blank=True, null=True)),
                ('product_id', models.CharField(blank=True, max_length=500, null=True)),
                ('category_id', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('order_no', models.IntegerField(blank=True, null=True)),
                ('banner_caption1', models.TextField(blank=True, null=True)),
                ('banner_caption2', models.TextField(blank=True, null=True)),
                ('is_notification_enabled_val', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('notification_msg', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isdeleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isblocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('category_banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_banners_images', to='webservices.EngageboostCategoryBanners')),
            ],
            options={
                'db_table': 'engageboost_category_banners_images',
            },
        ),
    ]