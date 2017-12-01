# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-06 18:34
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def move_event_page_data_to_event(event):
    """Copies data from event page to event"""
    try:
        page = event.eventpage
    except ObjectDoesNotExist:
        print('Missing event page:', event.name, event.date, event.pk)
    else:
        event.page_title = page.title or ''
        event.page_description = page.description or ''
        event.page_main_color = page.main_color or ''
        event.page_custom_css = page.custom_css or ''
        event.page_url = page.url or ''
        event.is_page_live = page.is_live
        event.save()


def move_data(apps, schema_editor):
    Event = apps.get_model('core', 'Event')
    EventPageContent = apps.get_model('core', 'EventPageContent')
    EventPageMenu = apps.get_model('core', 'EventPageMenu')
    for event in Event.objects.select_related('eventpage'):
        move_event_page_data_to_event(event)
    for content in EventPageContent.objects.select_related('page__event'):
        content.event = content.page.event
        content.save()
    for menu in EventPageMenu.objects.select_related('page__event'):
        menu.event = menu.page.event
        menu.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20170106_1833'),
    ]

    operations = [
        migrations.RunPython(move_data, migrations.RunPython.noop)
    ]
