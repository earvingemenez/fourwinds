# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 01:47
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_add_safety_insurance_right_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='websitesafetyinsuranceindexpage',
            old_name='body',
            new_name='body_left',
        ),
        migrations.AddField(
            model_name='websitesafetyinsuranceindexpage',
            name='body_bottom',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]