from django.urls import path
from main.views.product import ProductsByCategoryView, ProductSingleView

urlpatterns = [
    path('category/<int:categoryId>', ProductsByCategoryView.as_view(), name='products-by-category-list'),
    path('<int:id>', ProductSingleView.as_view(), name='product-by-id')
]