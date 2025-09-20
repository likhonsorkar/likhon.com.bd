from django.contrib import admin
from django.utils.html import format_html
from apps.shop.models import (
    ProductCategory,
    Product,
    ProductImage,
    ProductAttribute,
    ProductVariation,
    Coupon,
    ShippingMethod,
    PaymentMethod,
    Order,
    OrderItem,
)



# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# Inline for Product Variations
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_by')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock_quantity', 'is_active', 'created_by')
    list_filter = ('is_active', 'is_featured', 'categories')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariationInline]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'price', 'stock_quantity', 'is_active', 'created_by', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'created_by', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    thumbnail.short_description = 'Thumbnail'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'amount', 'expiry_date', 'created_by')


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'created_by')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status',)
    date_hierarchy = 'created_at'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variation', 'quantity', 'price', 'created_by')


# # from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from apps.shop.models import (
#     ProductCategory,
#     Product,
#     ProductAttribute,
#     ProductVariation,
#     Coupon,
#     ShippingMethod,
#     PaymentMethod,
#     Order,
#     OrderItem,
#     ProductImage
# )

# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'parent', 'created_by')
#     prepopulated_fields = {"slug": ("name",)}

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'sku', 'price', 'stock_quantity', 'is_active', 'created_by')
#     list_filter = ('is_active', 'is_featured', 'categories')
#     search_fields = ('name', 'sku')
#     prepopulated_fields = {"slug": ("name",)}

# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_by')

# @admin.register(ProductVariation)
# class ProductVariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'sku', 'price', 'stock_quantity', 'is_active', 'created_by')

# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = ('code', 'discount_type', 'amount', 'expiry_date', 'created_by')

# @admin.register(ShippingMethod)
# class ShippingMethodAdmin(admin.ModelAdmin):
#     list_display = ('name', 'cost', 'created_by')

# @admin.register(PaymentMethod)
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_by')

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'status', 'total', 'created_at')
#     list_filter = ('status',)
#     date_hierarchy = 'created_at'

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'variation', 'quantity', 'price', 'created_by')

