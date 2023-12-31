from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    SORT_MAP = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }

    phones = Phone.objects.all()

    sort = request.GET.get('sort', None)
    if sort:
        phones = phones.order_by(SORT_MAP[sort])

    template = 'catalog.html'
    context = {
        'phones': phones
    }
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.get(slug=slug)
    template = 'product.html'
    context = {
        'phone': phone
    }
    return render(request, template, context)
