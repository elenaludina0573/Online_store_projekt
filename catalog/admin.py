from django.contrib import admin
from catalog.models import Category, Product, Version

admin.site.register(Version)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'purchase_price', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']


