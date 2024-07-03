import uuid
import random
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import Count, Sum, Avg, StdDev
from django.utils.translation import gettext_lazy as _

def generate_unique_category_id():
    return str(uuid.uuid4()).replace('-', '')

class Banner(models.Model):
 name = models.CharField(max_length=200, db_index=True)
 description = models.TextField(blank=True)
 ceiling = models.PositiveIntegerField()
 image = models.ImageField(upload_to='banners/%Y/%m/%d', blank=True)
 created = models.DateTimeField(auto_now_add=True)
 updated = models.DateTimeField(auto_now=True)

 class Meta:
  ordering = ('name',)
  verbose_name = 'banner'
  verbose_name_plural = 'banners'

 def __str__(self):
  return self.name
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category_id = models.CharField(max_length=300, unique=True, default=generate_unique_category_id, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @staticmethod
    def get_categories_with_product_counts():
        return Category.objects.annotate(product_count=Count('products'))

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_with_category():
        return Product.objects.select_related('category')

    @staticmethod
    def get_top_selling_products(limit=10):
        return Product.objects.order_by('?')[:limit]
    
    @staticmethod
    def get_average_selling_products():
        avg_sales = Product.objects.all().aggregate(avg_sales=Avg('sell_count'))['avg_sales']
        stddev_sales = Product.objects.all().aggregate(stddev_sales=StdDev('sell_count'))['stddev_sales']
        return Product.objects.filter(sell_count__gte=avg_sales - stddev_sales, sell_count__lte=avg_sales + stddev_sales)[:3]
    @staticmethod
    def get_recommended_products():
        products = list(Product.objects.order_by('-sell_count'))
        return random.sample(products, min(len(products), 5))
    @staticmethod
    def get_new_products(days=30):
        cutoff_date = timezone.now() - timedelta(days=days)
        return Product.objects.filter(created__gte=cutoff_date).order_by('-created')[:5]
    @property
    def price_int(self):
        return int(str(self.price).split('.')[0])

    @property
    def old_price_int(self):
        return int(str(self.old_price).split('.')[0])
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=200, blank=True)
    village = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    number_home = models.CharField(max_length=100, blank=True, null=True)
    delivery_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    @staticmethod
    def get_orders_with_items():
        return Order.objects.prefetch_related('items')

    @staticmethod
    def get_total_sales():
        return Order.objects.aggregate(total_sales=Sum('items__price'))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    @staticmethod
    def get_order_items_with_products():
        return OrderItem.objects.select_related('product')

class Cart(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    all_price = models.PositiveIntegerField(editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
    def save(self, *args, **kwargs):
        self.all_price = self.quantity * self.product.price_int
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def __str__(self):
        return f'Cart item for product {self.product.name}'

    @staticmethod
    def get_cart_items_with_products():
        return Cart.objects.select_related('product')
