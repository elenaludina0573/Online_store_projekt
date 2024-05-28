from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Contacts, Blogpost, Version, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from pytils.translit import slugify


from config.services import get_cached_data


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    extra_context = {'title': 'Продукты на любой вкус'}

    # def get_queryset(self):
    #     return get_cached_data(self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты на любой вкус'
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_item = self.get_object()
        context['product_item'] = product_item
        context['title'] = f'Продукт #{product_item.id}'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_from.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить продукт'
        return context

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_from.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = ProductFormset(instance=self.object)
        context['title'] = 'Изменить продукт'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm('product.cancellation_of_publication')
                and user.has_perm('product.changes_the_description')
                and user.has_perm('product.changes_the_category')):
            return ProductModeratorForm
        else:
            return PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить продукт'
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return get_cached_data(self.model)


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'objects_list'


class ContactsView(ListView):
    model = Contacts
    extra_context = {'title': 'Контакты'}
    template_name = 'catalog/contacts_list.html'


class BlogpostListView(ListView):
    model = Blogpost
    template_name = 'catalog/blogpost_list.html'
    extra_context = {'title': ' Блоговая запись'}

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
            new_blog = form.save(commit=False)
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
