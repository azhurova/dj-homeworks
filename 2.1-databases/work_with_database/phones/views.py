from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort', None)

    if sort == 'name':
        sort_field_name = 'name'
    elif sort == 'min_price':
        sort_field_name = 'price'
    elif sort == 'max_price':
        sort_field_name = '-price'
    else:
        sort_field_name = None

    if sort_field_name:
        phones = Phone.objects.all().order_by(sort_field_name)
    else:
        phones = Phone.objects.all()
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
