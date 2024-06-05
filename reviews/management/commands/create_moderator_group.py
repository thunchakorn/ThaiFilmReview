from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Add all moderator's permission"
    perm_codenames = ["ban_comment", "mark_as_spoiler"]

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            moderator_group, _ = Group.objects.get_or_create(name="moderator")

            for codename in self.perm_codenames:
                perm = Permission.objects.get(codename=codename)
                moderator_group.permissions.add(perm)
        except Exception as e:
            raise CommandError("Command error", e)
