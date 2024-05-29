from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import (ProductDetailView, ProductListView, ContactsView, BlogpostListView, BlogpostCreateView,
                           BlogpostDeleteView, BlogpostUpdateView, BlogpostDetailView, ProductCreateView,
                           ProductUpdateView, ProductDeleteView, CategoryListView, CategoryDetailView)
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('catalog/create/', ProductCreateView.as_view(), name='product_form'),
    path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('contacts/', ContactsView.as_view(), name="contacts_list"),
    path('catalog/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('catalog/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('catalog/', BlogpostListView.as_view(), name='blogpost_list'),
    path('blogpost/create/', BlogpostCreateView.as_view(), name='blogpost_form'),
    path('blogpost/<int:pk>/', BlogpostDetailView.as_view(), name='blogpost_detail'),
    path('blogpost/<int:pk>/update/', BlogpostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost/<int:pk>/delete/', BlogpostDeleteView.as_view(), name='blogpost_delete'),
]
