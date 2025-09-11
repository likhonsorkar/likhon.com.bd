from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(ProductCategory, related_name='products')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_product_images')

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attributes')

    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    attributes = models.JSONField()  # Example: {"Size": "M", "Color": "Red"}
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/variations/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_variations')

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=50, choices=[('percent', 'Percent'), ('fixed', 'Fixed')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    usage_limit = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_coupons')

    def __str__(self):
        return self.code

class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_shipping_methods')

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payment_methods')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variation = models.ForeignKey(ProductVariation, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_order_items')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# from django.db import models
# from django.contrib.auth.models import User

# class ProductCategory(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     slug = models.SlugField(unique=True)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_categories')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
#     short_description = models.TextField(blank=True)
#     sku = models.CharField(max_length=100, unique=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     stock_quantity = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     is_featured = models.BooleanField(default=False)
#     categories = models.ManyToManyField(ProductCategory, related_name='products')
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class ProductAttribute(models.Model):
#     name = models.CharField(max_length=255)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attributes')

#     def __str__(self):
#         return self.name

# class ProductVariation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
#     attributes = models.JSONField()  # Example: {"Size": "M", "Color": "Red"}
#     sku = models.CharField(max_length=100, unique=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_variations')

#     def __str__(self):
#         return f"{self.product.name} - {self.sku}"

# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     discount_type = models.CharField(max_length=50, choices=[('percent', 'Percent'), ('fixed', 'Fixed')])
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     usage_limit = models.IntegerField(null=True, blank=True)
#     expiry_date = models.DateTimeField(null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_coupons')

#     def __str__(self):
#         return self.code

# class ShippingMethod(models.Model):
#     name = models.CharField(max_length=255)
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_shipping_methods')

#     def __str__(self):
#         return self.name

# class PaymentMethod(models.Model):
#     name = models.CharField(max_length=255)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payment_methods')

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
#     status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
#     coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     variation = models.ForeignKey(ProductVariation, null=True, blank=True, on_delete=models.SET_NULL)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_order_items')

#     def __str__(self):
#         return f"{self.product.name} x {self.quantity}"