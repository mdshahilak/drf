# Generated by Django 5.0.6 on 2024-07-08 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_alter_person_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="team_name",
            field=models.CharField(max_length=255),
        ),
    ]
