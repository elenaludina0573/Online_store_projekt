from django.urls import path
from catalog.views import product, home, contacts
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path("contacts/", contacts, name="contacts"),
    path('catalogs/<int:pk>', product, name='product'),

]
