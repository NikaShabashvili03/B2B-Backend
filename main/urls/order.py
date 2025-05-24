from django.urls import path
from ..views.order import SubmitOrderView, MyOrdersView



urlpatterns = [
    path('submit', SubmitOrderView.as_view()),
    path('my', MyOrdersView.as_view())
]