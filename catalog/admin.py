from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'purchase_price', 'categoty']
    list_filter = ['categoty']
    search_fields = ['name', 'description']


