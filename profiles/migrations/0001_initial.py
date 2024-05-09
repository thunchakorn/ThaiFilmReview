# Generated by Django 5.0.4 on 2024-05-08 07:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("bio", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "profile_pic",
                    models.ImageField(blank=True, null=True, upload_to="profile_pic/"),
                ),
                ("slug", models.SlugField(blank=True, default="", max_length=200)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "followings",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="followers",
                        to="profiles.profile",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
