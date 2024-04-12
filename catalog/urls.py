from django.urls import path
from catalog.views import index_1, contact, index
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('index/', index, name='index'),
    path('', index_1, name='index_1'),
    path('contacts/', contact, name='contacts')
]

