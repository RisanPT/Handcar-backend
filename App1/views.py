from random import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from twilio.rest import Client
import random
from django.core.cache import cache
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, WishlistItem, CartItem


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Get user details from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if all fields are provided
        if not all([name, email, phone, password]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format'}, status=400)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already taken'}, status=400)

        # Check if the phone number is already registered
        if User.objects.filter(username=phone).exists():
            return JsonResponse({'error': 'Phone number is already registered'}, status=400)

        # Create the user
        user = User.objects.create(
            username=phone,  # Using phone as the username
            first_name=name,
            email=email,
            password=make_password(password)  # Hash the password
        )

        # Respond with success
        return JsonResponse({'message': 'Signup successful!'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')  # Get the phone number from the request

        if not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)

        try:
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            # Generate the OTP
            otp = generate_otp()
            message_body = f"Your OTP code is {otp}"

            # Send the OTP via Twilio
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            # Return success response with the message SID
            return JsonResponse({'message': 'OTP sent successfully', 'sid': message.sid}, status=200)

        except Exception as e:
            # Handle any errors and return a failure response
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def generate_otp(length=6):
    """Generates a random OTP of the given length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# Store OTP in cache for 5 minutes (300 seconds)
OTP_EXPIRATION_TIME = 300  # 5 minutes

def store_otp(phone, otp):
    """Stores the OTP in cache with expiration"""
    cache.set(phone, otp, timeout=OTP_EXPIRATION_TIME)

def verify_otp(phone, entered_otp):
    """Verifies if the entered OTP matches the stored one"""
    stored_otp = cache.get(phone)  # Retrieves the stored OTP from cache
    if stored_otp and stored_otp == entered_otp:
        # OTP is correct, remove it from the cache after verification
        cache.delete(phone)
        return True
    return False

# View for logging in with a password
@csrf_exempt
def login_with_password(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Assuming you are using phone as the username field
        try:
            user = User.objects.get(username=phone)
            user = authenticate(request, username=phone, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# View for logging in with OTP  NOT WORKING- SHOWING INVALID OTP ERROR
@csrf_exempt
def login_with_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        entered_otp = request.POST.get('otp')

        # Verify OTP
        if verify_otp(phone, entered_otp):
            # Log in the user by phone number, assuming phone is the username
            try:
                user = User.objects.get(username=phone)
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            # If the item is already in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'message': 'Product added to cart', 'cart_quantity': cart_item.quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# @csrf_exempt
# @login_required
# def add_to_wishlist(request, product_id):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, id=product_id)
#         wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

@csrf_exempt
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

        # Return a JSON response with a success message or redirect
        if created:
            return JsonResponse({'message': 'Product added to wishlist', 'product_id': product_id})
        else:
            return JsonResponse({'message': 'Product already in wishlist', 'product_id': product_id})

    # If not a POST request, return a 405 Method Not Allowed
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def product_search(request):
    query = request.GET.get('search')
    accessories = Product.objects.all()

    if query:
        accessories = accessories.filter(name__icontains=query)  # Filter by name, case-insensitive

    # Prepare data for JSON response
    accessories_data = [
        {
            'id': accessory.id,
            'name': accessory.name,
            'price': accessory.price,
            'brand': accessory.brand.name,  # Get the brand name instead of the brand object
            'image_url': accessory.image.url if accessory.image and hasattr(accessory.image, 'url') else None,
            'description': accessory.description,
        }
        for accessory in accessories
    ]

    return JsonResponse({'accessories': accessories_data, 'query': query})


def filter_by_category(queryset, category_id):
    return queryset.filter(category_id=category_id)


def filter_by_aed(queryset, min_price=None, max_price=None):
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    return queryset


def filter_by_brand(queryset, brand_id):
    return queryset.filter(brand_id=brand_id)


from django.utils import timezone
from datetime import timedelta

def filter_by_new_arrivals(queryset, days=30):
    recent_date = timezone.now() - timedelta(days=days)
    return queryset.filter(created_at__gte=recent_date)


def filter_by_rating(queryset, min_rating):
    return queryset.filter(rating__gte=min_rating)

@csrf_exempt
def filter_products(request):
    products = Product.objects.all()

    # Get filter parameters from request
    category_id = request.GET.get('category_id')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand_id = request.GET.get('brand_id')
    min_rating = request.GET.get('min_rating')
    new_arrivals = request.GET.get('new_arrivals')  # Expects something like 'true'

    # Apply filters
    if category_id:
        products = filter_by_category(products, category_id)

    if min_price or max_price:
        products = filter_by_aed(products, min_price=min_price, max_price=max_price)

    if brand_id:
        products = filter_by_brand(products, brand_id)

    if min_rating:
        products = filter_by_rating(products, min_rating)

    if new_arrivals == 'true':  # Check if new arrivals filter is requested
        products = filter_by_new_arrivals(products)

    # Prepare data for JSON response
    products_data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'brand': product.brand.name,
            'image_url': product.image.url if product.image else None,
            'description': product.description,
            'rating': product.rating,
        }
        for product in products
    ]

    return JsonResponse({'products': products_data})





import logging
from django.http import JsonResponse, HttpResponseBadRequest
from urllib.parse import quote
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def subscribe(request):
    logger.info("subscribe view called")  # Log when the view is hit

    if request.method == 'POST':
        plan = request.POST.get('plan')
        category = request.POST.get('category')
        duration = request.POST.get('duration')

        if plan and category and duration:
            message = f"I would like to subscribe to the {plan} plan for {category} for {duration}."
            encoded_message = quote(message)
            whatsapp_url = f"https://wa.me/917025791186?text={encoded_message}"

            logger.info(f"Generated WhatsApp URL: {whatsapp_url}")  # Log the generated URL

            return JsonResponse({'whatsapp_url': whatsapp_url})
        else:
            logger.warning("Invalid subscription data")
            return HttpResponseBadRequest("Invalid subscription data.")

    logger.warning("Invalid request method")
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def display_cart(request):
    if request.user.is_authenticated:
        # Get all cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)

        # Prepare cart items data for JSON response
        cart_data = []
        for item in cart_items:
            cart_data.append({
                'product_name': item.product.name,
                'product_price': item.product.price,
                'quantity': item.quantity,
                'total_price': item.product.price * item.quantity,
            })

        # Calculate total price for the cart
        total_price = sum(item['total_price'] for item in cart_data)

        # Return JSON response with cart items and total price
        return JsonResponse({
            'cart_items': cart_data,
            'total_price': total_price
        })

    return JsonResponse({'error': 'User not authenticated'}, status=401)

def remove_cart_item(request, item_id):
    if request.user.is_authenticated:
        # Get the cart item based on the ID and user
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

        # Delete the cart item
        cart_item.delete()

        # Get all remaining cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)

        # Prepare cart items data for JSON response
        cart_data = []
        for item in cart_items:
            cart_data.append({
                'product_name': item.product.name,
                'product_price': item.product.price,
                'quantity': item.quantity,
                'total_price': item.product.price * item.quantity,
            })

        # Calculate total price for the cart after removal
        total_price = sum(item['total_price'] for item in cart_data)

        # Return updated cart data
        return JsonResponse({
            'message': 'Item removed successfully',
            'cart_items': cart_data,
            'total_price': total_price
        })

    return JsonResponse({'error': 'User not authenticated'}, status=401)

