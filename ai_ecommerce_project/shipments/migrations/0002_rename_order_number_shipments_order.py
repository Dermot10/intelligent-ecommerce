# Generated by Django 4.2.16 on 2025-01-18 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shipments", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shipments", old_name="order_number", new_name="order",
        ),
    ]
