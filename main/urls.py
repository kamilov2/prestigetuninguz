from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('add_to_cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('basket/', views.BasketView.as_view(), name='basket_view'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('cart/increase/<int:item_id>/', views.IncreaseQuantityView.as_view(), name='counter_plus'),
    path('cart/decrease/<int:item_id>/', views.DecreaseQuantityView.as_view(), name='counter_minus'),
    path('clear_basket/', views.ClearBasketView.as_view(), name='clear_basket'),
    path('clear_basket_by_id/<int:item_id>/', views.ClearBasketByIdView.as_view(), name='clear_basket_by_id'),
    path('filter/', views.FilterView.as_view(), name='filter'),
    path('search', views.SearchView.as_view(), name='search'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', views.CheckoutSuccessView.as_view(), name='checkout_success'),
    path('order/delivery', views.DeliveryView.as_view(), name='delivery'),
    path('order/comming', views.CommingView.as_view(), name='comming'),
    path('tuning_product/', views.TunningView.as_view(), name='tuning_product'), 
]
