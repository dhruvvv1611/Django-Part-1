from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields: list[str] = ['collection']
    prepopulated_fields = {
        'slug': ['title'],
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_per_page = 10
    list_editable = ['unit_price']
    list_select_related = ['collection']


    def collection_title(self, product):
        return product.collection.title


    @admin.display(
        ordering='inventory',
        description='Inventory Status'
    )
    def inventory_status(self, product):
        return "Low Stock" if product.inventory < 10 else "In Stock"
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
      upadated_count = queryset.update(inventory=0)
      self.message_user(request, f'{upadated_count} products were updated')
      messages.error(request, f'{upadated_count} products were updated')



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id','customer', 'placed_at', ]
    list_per_page = 10
    ordering = ['placed_at']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def order_count(self, customer):
        url = reverse('admin:store_order_changelist') + f'?customer__id__exact={customer.id}'
        return format_html('<a href="{}">{}</a>', url, customer.order_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_filter = ['title']
    search_fields = ['title']
    

    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + f'?collection__id__exact={collection.id}'

        return format_html('<a href = "{}">{}</a>', url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')  
        )

   
    

