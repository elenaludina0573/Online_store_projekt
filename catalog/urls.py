from django.urls import path
from catalog.views import (ProductDetailView, ProductListView, ContactsView, BlogpostListView, BlogpostCreateView,
                           BlogpostDeleteView, BlogpostUpdateView, BlogpostDetailView)
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactsView.as_view(), name="contacts"),
    path('catalog/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/', BlogpostListView.as_view(), name='blogpost_list'),
    path('catalog/create/', BlogpostCreateView.as_view(), name='blogpost_form'),
    path('catalog/<int:pk>/', BlogpostDetailView.as_view(), name='blogpost_detail'),
    path('catalog/<int:pk>/update/', BlogpostUpdateView.as_view(), name='blogpost_update'),
    path('catalog/<int:pk>/delete/', BlogpostDeleteView.as_view(), name='blogpost_delete'),
]
