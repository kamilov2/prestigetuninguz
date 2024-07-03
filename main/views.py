import telebot
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views import View
from .models import Banner, Category, Product, Cart, Order, OrderItem
from django.db.models import Count

TELEGRAM_BOT_TOKEN = '6704792126:AAGpqxtc36goOtl62kKQpCSXEzp9d2sQ-iY'
TELEGRAM_CHAT_ID_DELIVERY = '-1002165196907' 

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


class HomePageView(View):
    template_name = 'index.html'

    def get(self, request):
        banners = Banner.objects.all().order_by('-id')[:3]
        average_selling_products = Product.get_average_selling_products()
        recommended_products = Product.get_recommended_products()
        new_products = Product.get_new_products()
        category_product_counts = dict(
            Category.objects.annotate(product_count=Count('products')).values_list('category_id', 'product_count')
        )
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_items = Cart.objects.filter(session_key=session_key).select_related('product').count()

        context = {
            'banners': banners,
            'average_selling_products': average_selling_products,
            'recommended_products': recommended_products,
            'new_products': new_products,
            'category_product_counts': category_product_counts,
            'cart_items': cart_items
        }

        return render(request, self.template_name, context)


class CategoryView(View):
    template_name = 'catalog.html'

    def get(self, request, category):
        category_obj = get_object_or_404(Category, category_id=category)
        
        products = Product.objects.filter(category=category_obj).order_by('-id')
        
        highest_price_product = Product.objects.all().order_by('price').first()
        
        lowest_price_product = Product.objects.all().order_by('-price').first()
        category_list = Category.objects.all()[:6]
        highest_price = highest_price_product.price_int if highest_price_product else None
        lowest_price = lowest_price_product.price_int if lowest_price_product else None

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            if int(page_number) < 1:
                page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(paginator.num_pages)

        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()

        context = {
            'category': category_obj,
            'page_obj': page_obj,
            'page_number': page_number,
            'highest_price_product': highest_price_product,
            'lowest_price_product': lowest_price_product,
            'highest_price': highest_price,
            'lowest_price': lowest_price,
            'total_items': total_items,
            "products": page_obj,
            "category_list": category_list
        }

        return render(request, self.template_name, context)


class ProductFilter:
    def __init__(self, categories=None, min_price=None, max_price=None):
        self.categories = categories
        self.min_price = min_price
        self.max_price = max_price

    def filter_products(self):
        products = Product.objects.all()

        if self.categories:
            products = products.filter(category__in=self.categories)

        if self.min_price:
            products = products.filter(price__gte=self.min_price)

        if self.max_price:
            products = products.filter(price__lte=self.max_price)

        return products

class FilterView(View):
    template_name = 'catalog.html'
    paginate_by = 6

    def get(self, request):
        category_ids = request.GET.getlist('categories')  

        if category_ids:
            categories = Category.objects.filter(category_id__in=category_ids)
        else:
            categories = None

        product_filter = ProductFilter(categories=categories, 
                                       min_price=request.GET.get('min_price'), 
                                       max_price=request.GET.get('max_price'))
        products = product_filter.filter_products()
        
        highest_price_product = products.order_by('price').first()
        lowest_price_product = products.order_by('-price').first()
        highest_price = highest_price_product.price_int if highest_price_product else None
        lowest_price = lowest_price_product.price_int if lowest_price_product else None
        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            if int(page_number) < 1:
                page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(paginator.num_pages)

        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()
        category_list = Category.objects.all()[:6]
        
        context = {
            'categories': categories,
            'page_obj': page_obj,
            'page_number': page_number,
            'highest_price_product': highest_price_product,
            'lowest_price_product': lowest_price_product,
            'total_items': total_items,
            'category_list': category_list,
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'products': page_obj,
            'highest_price': highest_price,
            'lowest_price': lowest_price
        }

        return render(request, self.template_name, context)

class SearchView(View):
    template_name = 'catalog.html'
    paginate_by = 6

    def get(self, request):
       
        search_query = request.GET.get('search')

        products = Product.objects.all()

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        categories = Category.objects.all()

        highest_price_product = products.order_by('price').first()
        lowest_price_product = products.order_by('-price').first()
        highest_price = highest_price_product.price_int if highest_price_product else None
        lowest_price = lowest_price_product.price_int if lowest_price_product else None

        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            if int(page_number) < 1:
                page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(paginator.num_pages)

        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()
        category_list = Category.objects.all()[:6]

        context = {
            'categories': categories,
            'page_obj': page_obj,
            'page_number': page_number,
            'highest_price_product': highest_price_product,
            'lowest_price_product': lowest_price_product,
            'total_items': total_items,
            'category_list': category_list,
            'products': page_obj,
            'highest_price': highest_price,
            'lowest_price': lowest_price,
            'search_query': search_query
        }

        return render(request, self.template_name, context)

class AddToCartView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        session_key = request.session.session_key

        cart_item, created = Cart.objects.get_or_create(
            session_key=session_key,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('main:basket_view')


class BasketView(View):
    template_name = 'basket.html'

    def get(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()
        total_price = sum(item.product.price_int * item.quantity for item in cart_items)

        context = {
            'cart': cart_items,
            'total_items': total_items,
            'total_price': total_price,
        }
        return render(request, self.template_name, context)


class SupportView(View):
    def get(self, request):

        return redirect('main:home_page')


class IncreaseQuantityView(View):
    def get(self, request, item_id):
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('http://127.0.0.1:8000/basket/#{}'.format(item_id))


class DecreaseQuantityView(View):
    def get(self, request, item_id):
        cart_item = get_object_or_404(Cart, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('http://127.0.0.1:8000/basket/#{}'.format(item_id))


class ClearBasketView(View):
    def get(self, request):
        session_key = request.session.session_key
        Cart.objects.filter(session_key=session_key).delete()
        return redirect('main:basket_view')
class ClearBasketByIdView(View):
    def get(self, request, item_id):
        session_key = request.session.session_key
        Cart.objects.filter(id=item_id).delete()
        return redirect('main:basket_view')
    





class CheckoutView(View):
    template_name = 'order.html'

    def get(self, request):
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()
        total_price = sum(item.product.price_int * item.quantity for item in cart_items)

        context = {
            'cart': cart_items,
            'total_items': total_items,
            'total_price': total_price,
        }
        return render(request, self.template_name, context)
    

class CheckoutSuccessView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(session_key=request.session.session_key).select_related('product')
        total_items = cart_items.count()
        context = {
            'total_items': total_items
        }
        
        return render(request, 'accepted.html', context)
    
class DeliveryView(View):

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        village = request.POST.get('village')
        street = request.POST.get('street')
        house = request.POST.get('home')
        comment = request.POST.get('message_for_delivery')
        session_key = request.session.session_key

        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        
        message_text = (
            f"<b>#dostavka:</b>\n\n"
            f"<b>Ism:</b> {name}\n"
            f"<b>Telefon raqami:</b> {phone}\n"
            f"<b>Shahar:</b> {city}\n"
            f"<b>Tuman:</b> {village}\n"
            f"<b>Kocha:</b> {street}\n"
            f"<b>Uy:</b> {house}\n"
            f"<b>Yetkazib beruvchi uchun komentariy:</b> {comment}\n\n"
            f"<b>Tovarlar:</b>\n"
        )

        total_price = 0
        for item in cart_items:
            message_text += (
                f"- {item.product.name}: {item.quantity} x {item.product.price_int}$ = {item.quantity * item.product.price}\n"
            )
            total_price += item.quantity * item.product.price_int

        message_text += f"\n<b>Umumiy summa:</b> {total_price}$"

        bot.send_message(TELEGRAM_CHAT_ID_DELIVERY, message_text, parse_mode='HTML')

        order = Order.objects.create(
            first_name=name,
            address=f"{city}, {village}, {street}, {house}",
            city=city,
            village=village,
            street=street,
            number_home=house,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.sell_count += item.quantity
            item.product.save()

        cart_items.delete()

        return redirect('main:checkout_success')
    
class CommingView(View):
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        session_key = request.session.session_key

        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        
        message_text = (
            f"<b>#olib_ketish:</b>\n\n"
            f"<b>Ism:</b> {name}\n"
            f"<b>Telefon raqami:</b> {phone}\n"
            f"<b>Tovarlar:</b>\n"
        )

        total_price = 0
        for item in cart_items:
            message_text += (
                f"- {item.product.name}: {item.quantity} x {item.product.price_int}$ = {item.quantity * item.product.price}\n"
            )
            total_price += item.quantity * item.product.price_int

        message_text += f"\n<b>Umumiy summa:</b> {total_price}$"

        bot.send_message(TELEGRAM_CHAT_ID_DELIVERY, message_text, parse_mode='HTML')

        order = Order.objects.create(
            first_name=name,
            address=f"none",
            city='none',
            village='none',
            street='none',
            number_home='none',
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.sell_count += item.quantity
            item.product.save()

        cart_items.delete()

        return redirect('main:checkout_success')


class TunningView(View):
    template_name = 'catalog.html'  
            
    def get(self, request):
        products = Product.objects.all().order_by('-id')[:30]
        
        highest_price_product = Product.objects.all().order_by('price').first()
        
        lowest_price_product = Product.objects.all().order_by('-price').first()
        category_list = Category.objects.all()[:6]
        highest_price = highest_price_product.price_int if highest_price_product else None
        lowest_price = lowest_price_product.price_int if lowest_price_product else None

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            if int(page_number) < 1:
                page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(paginator.num_pages)

        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
        total_items = cart_items.count()

        context = {
            'page_obj': page_obj,
            'page_number': page_number,
            'highest_price_product': highest_price_product,
            'lowest_price_product': lowest_price_product,
            'highest_price': highest_price,
            'lowest_price': lowest_price,
            'total_items': total_items,
            "products": page_obj,
            "category_list": category_list
        }

        return render(request, self.template_name, context)
