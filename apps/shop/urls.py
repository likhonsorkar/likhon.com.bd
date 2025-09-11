from django.urls import path
from apps.shop import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:cart_item_key>/', views.remove_from_cart, name='remove_from_cart'),

    # Seller Dashboard URLs
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/products/create/', views.create_product, name='create_product'),
    path('seller/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
