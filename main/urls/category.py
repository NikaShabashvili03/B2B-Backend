from django.urls import path
from main.views.category import CategoryView, CategorySingleView, CategoryAttributesView

urlpatterns = [
    path('view', CategoryView.as_view(), name='category-list'),
    path('view/<int:id>', CategorySingleView.as_view(), name='category-by-id'),
    path('view/<int:id>/attributes', CategoryAttributesView.as_view(), name='category-attributes')
]