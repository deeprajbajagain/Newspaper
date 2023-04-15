# Generated by Django 4.1.5 on 2023-02-09 02:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("newspaper", "0002_newsletter"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
