# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-07 13:49
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_migrate_stats_to_event'),
    ]

    operations = [
        migrations.RemoveField(model_name='postmortem', name='event'),
        migrations.DeleteModel(name='Postmortem'),
    ]
