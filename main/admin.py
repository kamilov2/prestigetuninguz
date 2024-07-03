from django.contrib import admin
from django.db.models import Count
from .models import Category, Product, Order, OrderItem, Cart, Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
 list_display = ('name', 'description', 'ceiling', 'created', 'updated')
 list_filter = ('created', 'updated')
 search_fields = ('name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'product_count')
    search_fields = ('name', 'category_id')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('products'))

    def product_count(self, obj):
        return obj.product_count
    product_count.admin_order_field = 'product_count'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sell_count', 'created', 'updated')
    list_filter = ('category', 'created', 'updated')
    search_fields = ('name', 'description')
    readonly_fields = ('created', 'updated')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'created', 'delivery_status')
    list_filter = ('created', 'delivery_status')
    search_fields = ('first_name', 'last_name', 'address', 'city', 'village', 'street')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')
    list_filter = ('order', 'product')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'product', 'quantity', 'all_price', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('session_key',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')
