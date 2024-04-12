from django.shortcuts import render
from catalog.models import Category


def index(request):
    return render(request, 'catalog/home.html')


def index_1(request, pk):
    context = {
         'object_list': Category.objects.get(pk=pk),
         'title': 'Магазин продуктов'
    }
    return render(request, 'catalog/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'catalog/contacts.html')
