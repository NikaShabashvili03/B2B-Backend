from django.urls import path, include

urlpatterns = [
    path('customer/', include('main.urls.customer')),
    path('cart/', include('main.urls.cart')),
    path('order/', include('main.urls.order')),
    path('category/', include('main.urls.category')),
    path('product/', include('main.urls.product'))
    # path('suppliers/', include('main.urls.suppliers')),
    # path('orders/', include('main.urls.orders'))
]