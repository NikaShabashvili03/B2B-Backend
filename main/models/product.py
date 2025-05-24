from django.db import models
from . import Category, Supplier

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    brand = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bulk_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Discounted price for bulk orders")
    stock_quantity = models.PositiveIntegerField(default=0)
    min_order_quantity = models.PositiveIntegerField(default=1, help_text="Minimum quantity for B2B orders")
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True)
    weight_kg = models.FloatField(blank=True, null=True)
    dimensions_cm = models.CharField(max_length=50, blank=True, null=True, help_text="LxWxH in cm")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    attributes = models.TextField(default="{}", blank=True)

    def __str__(self):
        return self.name