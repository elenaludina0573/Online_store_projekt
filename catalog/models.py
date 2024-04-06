from django.db import models
from datetime import datetime


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')
    description = models.TextField(**NULLABLE, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description = models.TextField(**NULLABLE, verbose_name='Описание продукта')
    picture = models.ImageField(upload_to='catalog/', **NULLABLE)
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    purchase_price = models.IntegerField(max_length=100, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
