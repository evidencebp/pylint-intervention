# Generated by Django 3.2.7 on 2021-09-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0054_alter_event_url_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="corona",
            field=models.BooleanField(
                default=False, verbose_name="Collect additional data for COVID-19 contact tracing"
            ),
        ),
    ]
