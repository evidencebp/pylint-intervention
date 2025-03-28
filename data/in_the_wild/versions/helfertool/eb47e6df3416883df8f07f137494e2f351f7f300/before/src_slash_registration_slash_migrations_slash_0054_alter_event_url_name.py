# Generated by Django 3.2.6 on 2021-08-12 16:44

import django.core.validators
from django.db import migrations, models
import registration.models.event


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0053_auto_20210808_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url_name',
            field=models.CharField(help_text='May contain the following chars: a-zA-Z0-9.', max_length=200, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]+$'), registration.models.event._validate_url_blocklist], verbose_name='Name for URL'),
        ),
    ]
