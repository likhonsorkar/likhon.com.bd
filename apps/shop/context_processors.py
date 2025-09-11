from .models import Product, ProductVariation

def cart(request):
    cart = request.session.get('cart', {})
    cart_items_count = 0
    for item in cart.values():
        cart_items_count += item.get('quantity', 0)
    return {'cart_items_count': cart_items_count}
