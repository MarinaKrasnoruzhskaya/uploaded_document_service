# Generated by Django 5.1.2 on 2024-10-24 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0002_alter_document_author"),
    ]

    operations = [
        migrations.RenameField(
            model_name="document",
            old_name="document_url",
            new_name="document",
        ),
    ]
