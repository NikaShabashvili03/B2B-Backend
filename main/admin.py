
from django.contrib import admin
from django import forms
from .models import Category, Product, Attribute, Supplier, Order, OrderItem, Customer, Cart, CartItem
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import Product, Attribute
import json

class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent')
    search_fields = ('name', 'description')
    inlines = [AttributeInline]
    
admin.site.register(Category, CategoryAdmin)

class ProductForm(forms.ModelForm):
    attributes_button = forms.CharField(
        label="Attributes",
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'value': 'Open Attributes',
            'class': 'btn btn-primary attribute-btn',
            'style': 'cursor: pointer;'
        }),
        required=False
    )

    # Hidden field to store the attributes as JSON
    attributes_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'brand', 'description', 'price', 'bulk_price', 
            'stock_quantity', 'min_order_quantity', 'sku', 'barcode', 'weight_kg',
            'dimensions_cm', 'supplier', 'attributes_button', 'attributes_data'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.instance.category if self.instance.pk else None
        if category:
            attributes = Attribute.objects.filter(category=category)
            for attribute in attributes:
                self.fields[f'attribute_{attribute.id}'] = forms.CharField(
                    label=attribute.name,
                    required=False,
                    widget=forms.TextInput(attrs={'placeholder': f'Enter {attribute.name} value'})
                )

            # Pre-fill the attributes_data hidden field with the current attributes of the product
            if self.instance.pk and self.instance.attributes:
                self.fields['attributes_data'].initial = self.instance.attributes

    def clean(self):
        cleaned_data = super().clean()

        # Ensure attributes data is retrieved and saved correctly
        attributes_data = self.cleaned_data.get('attributes_data', '{}')
        cleaned_data['attributes'] = attributes_data
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.attributes = self.cleaned_data['attributes']  # Save attributes as JSON
        if commit:
            instance.save()
        return instance


    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_quantity', 'sku')
    search_fields = ('name', 'sku', 'category__name')
    list_filter = ('category', 'supplier')

    form = ProductForm

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'admin/js/show_attributes_modal.js',
            ) 

admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)