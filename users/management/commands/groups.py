from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='moderator')
        if created:
            self.stdout.write(self.style.SUCCESS('Group created'))
            countent_type = ContentType.objects.get_for_model(Product)
            perm_cancellation_of_publication = Permission.objects.created(
                codename='cancellation_of_publication_command',
                name='Canceling the publication of the product',
                content_type=countent_type,
            )
            perm_changes_the_description = Permission.objects.created(
                codename='changes_the_description_command',
                name='Changes the description of the product',
                content_type=countent_type,
            )
            perm_changes_the_category = Permission.objects.created(
                codename='changes_the_category_command',
                name='Changes the category of the product',
                content_type=countent_type,
            )
            new_group.permissions.add(perm_cancellation_of_publication)
            new_group.permissions.add(perm_changes_the_description)
            new_group.permissions.add(perm_changes_the_category)
            self.stdout.write(self.style.SUCCESS('Group add permissions'))
            new_group.save()
        else:
            self.stdout.write(self.style.WARNING('Group already exists'))
