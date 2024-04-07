from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.conf import settings
import json
import os


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', 'catalog_data.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            category = []
            for object in data:
                if object.get('model') == 'catalog.category':
                    category.append(object)
            return category

    @staticmethod
    def json_read_products():
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', 'catalog_data.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            category = []
            for object in data:
                if object.get('model') == 'catalog.product':
                    category.append(object)
            return category

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создайте списки для хранения объектов
        category_for_create = []
        product_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_fields = category.get('fields')
            category_for_create.append(
                Category(id=category_fields.get('pk'), name=category_fields.get('name'),
                         description=category_fields.get('description'))
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_fields = product.get('fields')
            product_for_create.append(
                Product(id=product_fields.get('pk'), name=product_fields.get('name'),
                        description=product_fields.get('description'),
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product_fields.get('category')),
                        purchase_price=product_fields.get('purchase_price'),
                        created_at=product_fields.get('created_at'), updated_at=product_fields.get('updated_at')
                        )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
