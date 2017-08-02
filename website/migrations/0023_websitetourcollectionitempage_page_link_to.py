# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('website', '0022_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitetourcollectionitempage',
            name='page_link_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
    ]