# Generated by Django 5.0.4 on 2024-05-04 09:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Person",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Film",
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
                ("name", models.CharField(max_length=100)),
                ("release_date", models.DateField(null=True, blank=True)),
                (
                    "poster",
                    models.ImageField(
                        null=True,
                        blank=True,
                        upload_to="film_poster/",
                    ),
                ),
                ("genres", models.ManyToManyField(to="films.genre")),
                (
                    "directors",
                    models.ManyToManyField(
                        related_name="directed_films", to="films.person"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=200,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^[\\u0E00-\\u0E7Fa-zA-Z0-9_]+\\Z"
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Role",
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
                ("name", models.CharField(max_length=100, null=True, blank=True)),
                (
                    "film",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roles",
                        to="films.film",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="films.person"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Link",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.URLField(blank=True, null=True)),
                (
                    "film",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        to="films.film",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="film",
            name="actors",
            field=models.ManyToManyField(
                related_name="acted_films", through="films.Role", to="films.person"
            ),
        ),
    ]
