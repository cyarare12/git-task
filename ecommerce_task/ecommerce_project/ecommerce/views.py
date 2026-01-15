from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime, timedelta
import secrets
import hashlib
from .forms import UserRegistrationForm, StoreForm, ProductForm, ReviewForm
from .models import Profile, Store, Product, Order, OrderItem, Review, ResetToken

def home(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'ecommerce/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'ecommerce/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def vendor_dashboard(request):
    if request.user.profile.role != 'vendor':
        return redirect('home')
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'ecommerce/vendor_dashboard.html', {'stores': stores})

@login_required
def create_store(request):
    if request.user.profile.role != 'vendor':
        return redirect('home')
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()

            # Tweet about new store
            try:
                from .functions.tweet import Tweet
                tweet_text = f"New store open!\n🏪 {store.name}\n📝 {store.description}\n#ecommerce #newstore"
                tweet = {'text': tweet_text}
                Tweet().make_tweet(tweet)
            except Exception as e:
                print(f"Tweet failed: {e}")
                # Continue without failing the store creation

            return redirect('vendor_dashboard')
    else:
        form = StoreForm()
    return render(request, 'ecommerce/create_store.html', {'form': form})

@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = StoreForm(instance=store)
    return render(request, 'ecommerce/edit_store.html', {'form': form})

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        store.delete()
        return redirect('vendor_dashboard')
    return render(request, 'ecommerce/delete_store.html', {'store': store})

@login_required
def store_products(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = Product.objects.filter(store=store)
    return render(request, 'ecommerce/store_products.html', {'store': store, 'products': products})

@login_required
def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            # Tweet about new product
            try:
                from .functions.tweet import Tweet
                tweet_text = f"New product added!\n🛍️ {product.name}\n🏪 From {store.name}\n📝 {product.description}\n💰 ${product.price}\n#ecommerce #newproduct"
                tweet = {'text': tweet_text}
                Tweet().make_tweet(tweet)
            except Exception as e:
                print(f"Tweet failed: {e}")
                # Continue without failing the product creation

            return redirect('store_products', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'ecommerce/add_product.html', {'form': form, 'store': store})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store_products', store_id=product.store.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'ecommerce/edit_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('store_products', store_id=product.store.id)
    return render(request, 'ecommerce/delete_product.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()
    else:
        has_purchased = False
    return render(request, 'ecommerce/product_detail.html', {'product': product, 'reviews': reviews, 'has_purchased': has_purchased})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.verified = OrderItem.objects.filter(order__user=request.user, product=product).exists()
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'ecommerce/add_review.html', {'form': form, 'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'name': product.name, 'price': str(product.price), 'quantity': 1}
    request.session['cart'] = cart
    return redirect('product_list')

def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'ecommerce/cart.html', {'cart': cart, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total)
        for product_id, item in cart.items():
            product = Product.objects.get(id=int(product_id))
            OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=float(item['price']))
        # Send invoice email
        invoice_body = f"Order Total: ${total}\nItems:\n"
        for product_id, item in cart.items():
            invoice_body += f"{item['name']} - {item['quantity']} x ${item['price']}\n"
        email = EmailMessage('Invoice', invoice_body, 'noreply@example.com', [request.user.email])
        email.send()
        request.session['cart'] = {}
        return redirect('home')
    return render(request, 'ecommerce/checkout.html', {'cart': cart, 'total': total})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(16)
            expiry = timezone.now() + timedelta(minutes=5)
            ResetToken.objects.create(user=user, token=hashlib.sha1(token.encode()).hexdigest(), expiry_date=expiry)
            reset_url = request.build_absolute_uri(reverse('reset_password', args=[token]))
            email_msg = EmailMessage('Password Reset', f'Click here to reset: {reset_url}', 'noreply@example.com', [email])
            email_msg.send()
            messages.success(request, 'Reset email sent')
        except User.DoesNotExist:
            messages.error(request, 'Email not found')
    return render(request, 'ecommerce/forgot_password.html')

def reset_password(request, token):
    try:
        hashed_token = hashlib.sha1(token.encode()).hexdigest()
        reset_token = ResetToken.objects.get(token=hashed_token)
        if reset_token.expiry_date < timezone.now():
            reset_token.delete()
            messages.error(request, 'Token expired')
            return redirect('forgot_password')
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                reset_token.user.set_password(password)
                reset_token.user.save()
                reset_token.delete()
                messages.success(request, 'Password reset successfully')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
        return render(request, 'ecommerce/reset_password.html')
    except ResetToken.DoesNotExist:
        messages.error(request, 'Invalid token')
        return redirect('forgot_password')
