from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')
    description = models.TextField(**NULLABLE, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description = models.TextField(**NULLABLE, verbose_name='Описание продукта')
    picture = models.ImageField(upload_to='catalog/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    purchase_price = models.IntegerField(max_length=150, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contacts(models.Model):
    city = models.CharField(max_length=50, verbose_name="Страна")
    identity_nalog_number = models.IntegerField(verbose_name="ИНН")
    address = models.TextField(verbose_name="Адрес")
    slug = models.CharField(max_length=255, verbose_name="URL", **NULLABLE)

    def __str__(self):
        return f"{self.city} {self.identity_nalog_number} {self.address}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Blogpost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.CharField(max_length=255, verbose_name="URL", **NULLABLE)
    content = models.TextField(verbose_name="Контент")
    preview = models.ImageField(upload_to='catalog/', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication_sign = models.BooleanField(default=True, verbose_name="Опубликовать")
    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Version(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт",
                                on_delete=models.SET_NULL, **NULLABLE, )
    number_of_version = models.PositiveIntegerField(verbose_name="Номер версии продукта")
    name_of_versions = models.CharField(max_length=150, verbose_name="Название версии")
    is_active_version = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
