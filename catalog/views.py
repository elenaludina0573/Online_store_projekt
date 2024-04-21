from django.shortcuts import render
from catalog.models import Product, Contacts, Blogpost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты на любой вкус'
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_item = self.get_object()
        context['product_item'] = product_item
        context['title'] = f'Продукт #{product_item.id}'
        return context


class ContactsView(ListView):
    model = Contacts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class BlogpostListView(ListView):
    model = Blogpost

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = '__all__'
    template_name = 'catalog/blogpost_from.html'
    success_url = reverse_lazy('catalog:blogpost_form')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить запись в блог'
        return context


class BlogpostUpdateView(UpdateView):
    model = Blogpost
    fields = '__all__'
    template_name = 'catalog/blogpost_from.html'
    success_url = reverse_lazy('catalog:blogpost_form')


class BlogpostDetailView(DetailView):
    model = Blogpost
    template_name = 'catalog/blogpost_detail.html'
    success_url = reverse_lazy('catalog:blogpost_detail')


class BlogpostDeleteView(DeleteView):
    model = Blogpost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = '/catalog/blogpost/'





