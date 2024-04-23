from catalog.models import Product, Contacts, Blogpost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from pytils.translit import slugify


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
        context['title'] = ' Блоговая запись'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication_sign=True)
        return queryset


class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = ['title', 'content', 'preview', 'publication_sign', 'number_of_views']
    template_name = 'catalog/blogpost_from.html'
    success_url = reverse_lazy('catalog:blogpost_form')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить запись в блог'
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogpostUpdateView(UpdateView):
    model = Blogpost
    fields = ['title', 'preview', 'publication_sign', 'number_of_views']
    template_name = 'catalog/blogpost_from.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить запись в блоге'
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogpostDetailView(DetailView):
    model = Blogpost
    template_name = 'catalog/blogpost_detail.html'
    success_url = reverse_lazy('catalog:blogpost_detail')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        blogpost_item = self.get_object()
        context['blogpost_item'] = blogpost_item
        context['title'] = f'Запись в блоге #{blogpost_item.id}'
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogpostDeleteView(DeleteView):
    model = Blogpost
    success_url = reverse_lazy('catalog:blogpost_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить запись из блога'
        return context
