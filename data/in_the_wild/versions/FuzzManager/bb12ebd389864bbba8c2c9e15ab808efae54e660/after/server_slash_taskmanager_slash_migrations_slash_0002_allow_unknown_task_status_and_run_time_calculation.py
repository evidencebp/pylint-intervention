# Generated by Django 2.2.12 on 2020-07-22 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("taskmanager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pool",
            name="max_run_time",
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="created",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="decision_id",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="pool",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="taskmanager.Pool",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="task",
            unique_together={("task_id", "run_id")},
        ),
    ]
