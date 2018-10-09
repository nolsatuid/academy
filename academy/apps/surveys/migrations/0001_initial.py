# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-05 14:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_status', models.PositiveIntegerField(choices=[(1, 'Karyawan'), (2, 'Mahasiswa'), (3, 'Belum Bekerja'), (99, 'Lain-lain')])),
                ('working_status_other', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('graduate_channeled', models.BooleanField()),
                ('graduate_channeled_when', models.PositiveIntegerField(choices=[(1, 'Segera'), (99, 'Lain-lain')])),
                ('graduate_channeled_when_other', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='survey', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
