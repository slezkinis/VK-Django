from django.contrib import admin
from .models import Product, Order, ProductCategory, OrderElements, Vk_user
from django.shortcuts import reverse
from django.utils.html import format_html


class Order_elementsInline(admin.TabularInline):
    model = OrderElements


@admin.register(Vk_user)
class Vk_userAdmin(admin.ModelAdmin):
    readonly_fields = [
        'cart',
        'vk_id'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        'status'
    ]
    inlines = [
        Order_elementsInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'price',
    ]
    list_display_links = [
        'title',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'title',
        'category__title',
    ]



@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass