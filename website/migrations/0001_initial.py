# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 05:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('phone_ext', models.CharField(max_length=10)),
                ('contact_method', models.CharField(max_length=20)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('caption', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='EventPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=website.models.get_event_photos_path)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Event')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('education_department', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=50)),
                ('country', models.CharField(default='United States', max_length=50)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travelers', models.IntegerField()),
                ('grade_levels', models.CharField(max_length=50)),
                ('complementary_chaperones', models.IntegerField()),
                ('transportation', models.CharField(max_length=150)),
                ('preferred_airport', models.CharField(max_length=200)),
                ('meals_to_include', models.CharField(max_length=60)),
                ('budget', models.CharField(max_length=200)),
                ('reference_file', models.FileField(null=True, upload_to=website.models.get_quotes_files_path)),
                ('how_hear', models.CharField(max_length=150)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Customer')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Organization')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Customer')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Organization')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('draft', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Trip',
                'verbose_name_plural': 'Trips',
            },
        ),
        migrations.AddField(
            model_name='testimonial',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Trip'),
        ),
        migrations.AddField(
            model_name='quote',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Trip'),
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.EventCategory'),
        ),
    ]