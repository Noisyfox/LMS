# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0008_assignmentfile_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_week', models.PositiveSmallIntegerField()),
                ('end_week', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('l', 'Lecture'), ('t', 'Tutorial'), ('b', 'Lab')], max_length=1)),
                ('location', models.CharField(max_length=128)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.Unit')),
            ],
        ),
    ]
