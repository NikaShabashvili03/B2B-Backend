from django.urls import path
from ..views.cart import CartView



urlpatterns = [
    path('', CartView.as_view()),
]