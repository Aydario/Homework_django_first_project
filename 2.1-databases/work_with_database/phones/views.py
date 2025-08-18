from django.shortcuts import render, redirect, get_object_or_404
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    
    sort = request.GET.get('sort', 'name')
    sort_mapping = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price'
    }
    order_by = sort_mapping.get(sort, 'name')
    
    phones = Phone.objects.all().order_by(order_by)
    
    context = {
        'phones': phones,
        'sort': sort
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    
    context = {
        'phone': phone
    }
    return render(request, template, context)
