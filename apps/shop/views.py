from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from apps.shop.forms import ProductForm, ProductImageForm, ProductVariationForm
from apps.shop.models import Product, ProductImage, ProductVariation
from django.http import JsonResponse

def shop(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "shop.html", {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variation_id = request.POST.get('variation')
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    
    cart_item_key = str(product_id)
    if variation_id:
        cart_item_key += f'_{variation_id}'

    if cart_item_key in cart:
        cart[cart_item_key]['quantity'] += quantity
    else:
        cart[cart_item_key] = {'quantity': quantity, 'price': str(product.price)}
        if variation_id:
            variation = get_object_or_404(ProductVariation, id=variation_id)
            cart[cart_item_key]['price'] = str(variation.price)

    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for key, item in cart.items():
        product_id, variation_id = (key.split('_') + [None])[:2]
        product = get_object_or_404(Product, id=product_id)
        
        price = float(item['price'])
        quantity = item['quantity']
        subtotal = price * quantity
        total_price += subtotal

        cart_item = {
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
            'key': key
        }

        if variation_id:
            variation = get_object_or_404(ProductVariation, id=variation_id)
            cart_item['variation'] = variation

        cart_items.append(cart_item)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, cart_item_key):
    cart = request.session.get('cart', {})
    if cart_item_key in cart:
        del cart[cart_item_key]
        request.session['cart'] = cart
    return redirect('cart_detail')


@login_required
def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')

@login_required
def seller_products(request):
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'seller/product_list.html', {'products': products})

@login_required
def create_product(request):
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)
    VariationFormSet = modelformset_factory(ProductVariation, form=ProductVariationForm, extra=1)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        variation_formset = VariationFormSet(request.POST, request.FILES, queryset=ProductVariation.objects.none())
        
        if form.is_valid() and image_formset.is_valid() and variation_formset.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            form.save_m2m()

            for form in image_formset.cleaned_data:
                if form:
                    image = form['image']
                    ProductImage.objects.create(product=product, image=image, created_by=request.user)
            
            for form in variation_formset.cleaned_data:
                if form:
                    variation = form.save(commit=False)
                    variation.product = product
                    variation.created_by = request.user
                    variation.save()

            return redirect('seller_products')
    else:
        form = ProductForm()
        image_formset = ImageFormSet(queryset=ProductImage.objects.none())
        variation_formset = VariationFormSet(queryset=ProductVariation.objects.none())
        
    return render(request, 'seller/product_form.html', {
        'form': form, 
        'image_formset': image_formset, 
        'variation_formset': variation_formset
    })

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, created_by=request.user)
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3, can_delete=True)
    VariationFormSet = modelformset_factory(ProductVariation, form=ProductVariationForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))
        variation_formset = VariationFormSet(request.POST, request.FILES, queryset=ProductVariation.objects.filter(product=product))

        if form.is_valid() and image_formset.is_valid() and variation_formset.is_valid():
            form.save()
            image_formset.save()
            variation_formset.save()
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)
        image_formset = ImageFormSet(queryset=ProductImage.objects.filter(product=product))
        variation_formset = VariationFormSet(queryset=ProductVariation.objects.filter(product=product))

    return render(request, 'seller/product_form.html', {
        'form': form, 
        'image_formset': image_formset, 
        'variation_formset': variation_formset
    })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, created_by=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_products')
    return render(request, 'seller/product_confirm_delete.html', {'product': product})
