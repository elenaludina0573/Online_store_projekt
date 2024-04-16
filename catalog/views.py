from django.shortcuts import render
from catalog.models import Product


def home(request):
    context = {"object_list": Product.objects.all(),
               "title": "Продукты на любой вкус"}
    return render(request, "catalog/home.html", context)


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        "object": Product.objects.get(pk=pk),
        "title": product_item.name,
    }
    return render(request, "catalog/product.html", context=context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'catalog/contacts.html')
