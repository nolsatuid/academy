# Generated by Django 2.2.10 on 2020-09-09 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0012_authsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='site_desc',
            field=models.TextField(blank=True, null=True, verbose_name='Site Description'),
        ),
    ]