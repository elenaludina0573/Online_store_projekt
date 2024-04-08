import random

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = []
        for i in range(10):
            category_list.append(
                Category(
                    name=f'Category#{i+1}',
                    description=f'This is another category #{i+1}'
                )
            )

        Category.objects.bulk_create(category_list)

        category_id_list = list(Category.objects.all().values_list('id', flat=True))
        max_id = max(category_id_list)
        min_id = min(category_id_list)

        product_list = []
        for i in range(100):
            product_list.append(
                Product(
                    name=f'Product#{i}',
                    description=f'This is description for product #{i}',
                    category_id=random.randint(min_id, max_id),
                    purchase_price=random.random() * 1000
                )
            )

        Product.objects.bulk_create(product_list)