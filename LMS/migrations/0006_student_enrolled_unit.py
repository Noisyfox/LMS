# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0005_assignment_assignmentfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='enrolled_unit',
            field=models.ManyToManyField(to='LMS.Unit'),
        ),
    ]