from django.shortcuts import render
from catalog.models import Product


def home(request):
    products_list = Product.objects.order_by("updated_at")
    context = {"products": products_list[:5:-1], "title": "Продукты на любой вкус"}
    return render(request, "catalog/home.html", context)


def index(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        "product": Product.objects.filter(pk=pk),
        "title": product_item.name,
    }
    return render(request, "catalog/index.html", context=context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'catalog/contacts.html')
