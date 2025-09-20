from django import forms
from apps.shop.models import (
    Product, ProductCategory, ProductAttribute, ProductVariation,
    Order, OrderItem, Coupon, ShippingMethod, PaymentMethod, ProductImage
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_by', 'created_at', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500', 'rows': 5}),
            'short_description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500', 'rows': 2}),
            'sku': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'sale_price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
            'categories': forms.SelectMultiple(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'w-full text-gray-700'}),
            'alt_text': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
        }

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['attributes', 'sku', 'price', 'stock_quantity', 'image']
        widgets = {
            'attributes': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'sku': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full text-gray-700'}),
        }
