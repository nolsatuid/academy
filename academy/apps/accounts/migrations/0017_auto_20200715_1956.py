# Generated by Django 2.2.10 on 2020-07-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200430_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Student'), (2, 'Trainer'), (3, 'Company'), (4, 'Vendor')], null=True),
        ),
    ]
