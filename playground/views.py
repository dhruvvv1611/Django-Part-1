from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q 
from store.models import Product, OrderItem, Order, Collection

def say_hello(request):
    collection  = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    collection.save()

    Collection.objects.filter(pk=1).update(title='Games')

    return render(request, 'hello.html' )
