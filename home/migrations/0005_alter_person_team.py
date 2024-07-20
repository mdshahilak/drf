# Generated by Django 5.0.6 on 2024-07-08 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_remove_person_team_name_person_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="team",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="home.team",
            ),
        ),
    ]