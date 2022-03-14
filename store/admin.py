from django.contrib import admin
from store.models import Product, Transaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'price', 'file']


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ['buyer', 'seller', 'price']
