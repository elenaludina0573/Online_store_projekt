from django.urls import path
from catalog.views import index_1, contact, index
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('index_1/<int:pk>', index_1, name='index_1'),
    path('contacts/', contact, name='contacts')
]

