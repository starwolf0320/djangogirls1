# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-07 11:59
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_date_extensions.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0026_auto_20170107_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coorganizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Co-organizer',
                'verbose_name_plural': 'Co-organizers',
            },
        ),
        migrations.CreateModel(
            name='EventApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_date_extensions.fields.ApproximateDateField(validators=[core.validators.validate_approximatedate])),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('latlng', models.CharField(blank=True, max_length=30, null=True)),
                ('website_slug', models.SlugField()),
                ('main_organizer_email', models.EmailField(max_length=254)),
                ('main_organizer_first_name', models.CharField(max_length=30)),
                ('main_organizer_last_name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('about_you', models.TextField()),
                ('why', models.TextField()),
                ('involvement', models.CharField(choices=[('newcomer', 'I’ve never been to a Django Girls event'), ('attendee', 'I’m a former attendee'), ('coach', 'I’m a former coach'), ('organizer', 'I’m a former organizer'), ('contributor', 'I contributed to the tutorial or translations')], max_length=15)),
                ('experience', models.TextField()),
                ('venue', models.TextField()),
                ('sponsorhip', models.TextField()),
                ('coaches', models.TextField()),
                ('previous_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Event')),
            ],
            options={
                'permissions': (('can_accept_organize_application', 'Can accept Organize Applications'),),
            },
        ),
        migrations.AddField(
            model_name='coorganizer',
            name='event_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='organize.EventApplication'),
        ),
    ]
