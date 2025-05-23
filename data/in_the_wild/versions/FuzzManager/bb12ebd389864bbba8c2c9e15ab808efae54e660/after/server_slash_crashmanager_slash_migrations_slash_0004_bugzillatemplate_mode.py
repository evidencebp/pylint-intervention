# Generated by Django 2.2.20 on 2021-05-21 14:15

import crashmanager.models
from django.db import migrations
import enumfields.fields


def update_mode(apps, schema_editor):
    BugzillaTemplate = apps.get_model("crashmanager", "BugzillaTemplate")
    BugzillaTemplate.objects.exclude(comment="").update(
        mode=crashmanager.models.BugzillaTemplateMode.Comment
    )


class Migration(migrations.Migration):

    dependencies = [
        ("crashmanager", "0003_auto_20210429_0908"),
    ]

    operations = [
        migrations.AddField(
            model_name="bugzillatemplate",
            name="mode",
            field=enumfields.fields.EnumField(
                default="bug",
                enum=crashmanager.models.BugzillaTemplateMode,
                max_length=30,
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            update_mode,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
