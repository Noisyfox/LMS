# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0004_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('due_time', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Assignment')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Student')),
            ],
        ),
    ]