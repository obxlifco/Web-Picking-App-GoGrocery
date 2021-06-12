# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-12 12:07
from __future__ import unicode_literals

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('company_id', models.BigIntegerField(blank=True, null=True)),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('boost_url', models.CharField(blank=True, max_length=255, null=True)),
                ('website_url', models.CharField(blank=True, max_length=255, null=True)),
                ('company_logo', models.CharField(blank=True, max_length=255, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=255, null=True)),
                ('designation', models.CharField(blank=True, max_length=255, null=True)),
                ('image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('reset_password', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('issuperadmin', models.CharField(blank=True, choices=[('Y', 'Y'), ('N', 'N')], default='N', max_length=2, null=True)),
                ('lead_manager_id', models.IntegerField(blank=True, null=True)),
                ('createdby_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('modifiedby_id', models.IntegerField(blank=True, null=True)),
                ('modified_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('is_verified', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('verified_code', models.CharField(blank=True, max_length=30, null=True)),
                ('refferal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('google_login_id', models.CharField(blank=True, max_length=255, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('device_token_ios', models.TextField(blank=True, null=True)),
                ('device_token_android', models.TextField(blank=True, null=True)),
                ('user_type', models.CharField(blank=True, choices=[('backend', 'backend'), ('frontend', 'frontend')], default='frontend', max_length=10, null=True)),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EngageboostApplicableAutoresponders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_id', models.IntegerField()),
                ('applicable_chanel_id', models.IntegerField()),
                ('applicable_for', models.CharField(blank=True, choices=[('Channel', 'Channel'), ('Warehouse', 'Warehouse'), ('ShippingProvider', 'ShippingProvider')], default='Channel', max_length=20, null=True)),
                ('shipment_status', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(blank=True, null=True)),
                ('modified', models.DateField(blank=True, null=True)),
                ('createdby', models.IntegerField(default='0')),
                ('updatedby', models.IntegerField(default='0')),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'engageboost_applicable_autoresponders',
            },
        ),
        migrations.CreateModel(
            name='EngageboostCountries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(blank=True, max_length=2, null=True)),
                ('countries_iso_code_3', models.CharField(blank=True, max_length=3, null=True)),
                ('ebay_countrycode', models.CharField(blank=True, max_length=255, null=True)),
                ('address_format_id', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('createdby', models.IntegerField(blank=True, default='0', null=True)),
                ('updatedby', models.IntegerField(blank=True, default='0', null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'engageboost_countries',
            },
        ),
        migrations.CreateModel(
            name='EngageboostEmailTypeContents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_email_type_id', models.IntegerField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('emarketing_website_template_id', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('email_type', models.CharField(blank=True, choices=[('H', 'H'), ('T', 'T'), ('HT', 'HT')], default='T', max_length=2, null=True)),
                ('email_content', models.TextField(blank=True, null=True)),
                ('email_content_text', models.TextField(blank=True, null=True)),
                ('sms_subject', models.CharField(blank=True, max_length=256, null=True)),
                ('sms_content_text', models.TextField(blank=True, null=True)),
                ('reply_to_email', models.TextField(blank=True, null=True)),
                ('bcc', models.CharField(blank=True, max_length=255, null=True)),
                ('email_from', models.CharField(blank=True, max_length=255, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('file_name', models.CharField(blank=True, max_length=100, null=True)),
                ('auto_responder_applied_for', models.CharField(choices=[('Others', 'Others'), ('Order', 'Order')], default='Others', max_length=20, null=True)),
                ('shipment_status', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(blank=True, null=True)),
                ('modified', models.DateField(blank=True, null=True)),
                ('createdby', models.IntegerField(blank=True, null=True)),
                ('updatedby', models.IntegerField(blank=True, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'engageboost_email_type_contents',
            },
        ),
        migrations.CreateModel(
            name='EngageboostRolemasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.IntegerField()),
                ('group_id', models.BigIntegerField()),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('user_role_type', models.CharField(blank=True, default='Super Admin', max_length=255, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('created', models.DateField(blank=True, null=True)),
                ('modified', models.DateField(blank=True, null=True)),
                ('isdeleted', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('isblocked', models.CharField(blank=True, choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
                ('createdby', models.IntegerField(blank=True, default='0', null=True)),
                ('updatedby', models.IntegerField(blank=True, default='0', null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('language_id', models.IntegerField(blank=True, default='0', null=True)),
            ],
            options={
                'db_table': 'engageboost_rolemasters',
            },
        ),
        migrations.AddField(
            model_name='engageboostapplicableautoresponders',
            name='auto_responder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auto_responder', to='webservices.EngageboostEmailTypeContents'),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webservices.EngageboostCountries'),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webservices.EngageboostRolemasters'),
        ),
        migrations.AddField(
            model_name='engageboostusers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
