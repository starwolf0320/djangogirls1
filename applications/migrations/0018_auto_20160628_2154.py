# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 21:54
from __future__ import unicode_literals

from django.db import migrations


def deduplicate_applications(apps, schema_editor):
    Application = apps.get_model("applications", "Application")
    applications = Application.objects.values_list("form", "email").distinct()

    for form, email in applications:
        duplicates = (
            Application.objects
            .filter(form=form, email=email)
            .values_list('id', flat=True)
            .order_by('created')[1:]
        )
        Application.objects.filter(id__in=list(duplicates)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0017_auto_20160617_1646'),
    ]

    operations = [
        migrations.RunPython(deduplicate_applications),
    ]
