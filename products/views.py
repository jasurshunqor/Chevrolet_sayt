from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem


def home_view(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
    })


def product_list_view(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    })


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related': related,
    })


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{product.name} savatga qo'shildi!")
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Mahsulot savatdan o'chirildi.")
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Savatingiz bo'sh!")
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')

        if not address or not phone:
            messages.error(request, "Manzil va telefon raqamini kiriting!")
            return render(request, 'products/checkout.html', {'cart': cart})

        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total_price=cart.get_total(),
        )
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.get_final_price(),
            )
        cart.items.all().delete()
        messages.success(request, f"Buyurtmangiz #{order.id} muvaffaqiyatli qabul qilindi!")
        return redirect('order_list')

    return render(request, 'products/checkout.html', {'cart': cart})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_detail.html', {'order': order})
