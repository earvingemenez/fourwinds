# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('website', '0014_delete_old_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteTestimonialPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='website.WebsiteTestimonialPage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WebsiteTag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.AddField(
            model_name='websitetestimonialpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='website_websitetestimonialpagetag_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='websitetestimonialpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='website.WebsiteTestimonialPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]