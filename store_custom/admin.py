from django.contrib import admin
from store.admin import ProductAdmin, CustomerAdmin
from store.models import Product, Customer
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInLine(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]


class CustomCustomerAdmin(CustomerAdmin):
    inlines = [TagInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

admin.site.unregister(Customer)
admin.site.register(Customer, CustomCustomerAdmin)
