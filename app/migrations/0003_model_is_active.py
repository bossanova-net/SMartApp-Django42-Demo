# Generated by Django 5.1.2 on 2024-10-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_delete_serviceteam"),
    ]

    operations = [
        migrations.AddField(
            model_name="model",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
