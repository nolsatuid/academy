# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-14 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20180223_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
    ]