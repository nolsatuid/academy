# Generated by Django 2.2.10 on 2020-04-02 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0007_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Apperance', max_length=50)),
                ('logo_light', models.ImageField(blank=True, help_text='Akan digunakan pada latar terang', null=True, upload_to='images/settings')),
                ('logo_dark', models.ImageField(blank=True, help_text='Akan digunakan pada latar gelap', null=True, upload_to='images/settings')),
                ('site_name', models.CharField(max_length=50)),
                ('footer_title', models.CharField(blank=True, max_length=100, null=True)),
                ('color_theme', models.PositiveIntegerField(choices=[(1, 'Danger'), (2, 'Warning'), (3, 'Primary'), (4, 'Success'), (5, 'Dark')], default=1)),
                ('sidebar_color', models.PositiveIntegerField(choices=[(1, 'Light'), (2, 'Dark')], default=1)),
            ],
        ),
    ]
