# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 18:23
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_adding_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='website.WebsiteCategory'),
        ),
    ]