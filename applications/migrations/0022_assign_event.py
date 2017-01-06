# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-06 21:13
from __future__ import unicode_literals

from django.db import migrations


def assign_events(apps, schema_editor):
    Form = apps.get_model('applications', 'Form')
    for form in Form.objects.select_related('page__event'):
        form.event = form.page.event
        form.save()


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0021_form_event'),
        ('core', '0020_auto_20160815_1701')
    ]

    operations = [
        migrations.RunPython(assign_events, migrations.RunPython.noop)
    ]
