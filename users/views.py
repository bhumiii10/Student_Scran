from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from orders.models import Order, Cart, CartItem, OrderItem
from restaurants.models import MenuItem, Discount
from .forms import UserRegistrationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from decimal import Decimal


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        email = request.POST.get('email')  # Use email as the unique identifier
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role (student or vendor)

        if not role or not email:
            return HttpResponse("Role and email are required.")

        # Verify if email matches the role criteria (student or vendor)
        if not verify_role_based_on_email(role, email):
            return HttpResponse(f"Invalid email address for the selected role: {role}")

        # Use Django's machinery to attempt to see if the email/password combination is valid.
        user = authenticate(request, username=email, password=password)  # Authenticate using email, not username

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))  # Redirect to the homepage (make sure 'index' is a valid URL pattern)
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {email}, {password}")
            return HttpResponse("Invalid login.")

    # If it's not a POST request, render the login form
    return render(request, 'registrations/login.html')

# Register page (Sign up)
def register(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging: print the POST data
        form = UserRegistrationForm(request.POST)  # Create form instance with POST data
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the database

            login(request, user)
            messages.success(request, 'You have been registered successfully.')
            return redirect('profile')  # Redirect to profile page after registration
        else:
            messages.error(request, 'There were errors in your form.')

    else:
        form = UserRegistrationForm()  # Empty form for GET request

    return render(request, 'registrations/registration.html', {'form': form})


# Profile page (Shows user details and order history)
@login_required  # Only logged-in users can access this page
def profile(request):
    # Fetch the user's orders
    orders = Order.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()
    context = {'orders': orders, 'cart': cart}
    return render(request, 'users/profile.html', context)

# users/views.py
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.phone_number = request.POST.get('phone_number')  # Update phone_number
        user.address = request.POST.get('address')  # Update address
        user.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')
    return render(request, 'users/edit_profile.html')


def verify_role_based_on_email(role, email):
    """
    Verifies whether the email corresponds to the selected role (student or vendor).
    """
    if not isinstance(email, str):  # Ensure email is a string
        return False

    if role == 'student':
        # Check if the email ends with 'student.ac.uk'
        if not email.endswith('student.ac.uk'):
            return False
    elif role == 'vendor':
        # Check if the email ends with 'business.com'
        if not email.endswith('business.com'):
            return False
    else:
        return False

    return True


# users/views.py
@login_required
def cart_view(request):
    if request.user.is_authenticated:
        # Check if the user has an active cart
        cart = Cart.objects.filter(user=request.user, status='Active').first()

        if not cart:
            # If no cart exists for the user, create a new one
            cart = Cart.objects.create(user=request.user, status='Active')

        # Group cart items by restaurant
        cart_items_by_restaurant = {}
        for item in cart.items.all():
            restaurant = item.item.restaurant
            if restaurant not in cart_items_by_restaurant:
                cart_items_by_restaurant[restaurant] = []
            cart_items_by_restaurant[restaurant].append(item)

        # Calculate total price per item and overall total
        total = sum(item.total_price() for item in cart.items.all())

        # Calculate discounted total if a discount is applied
        discounted_total = None
        if 'discount' in request.session:
            discount_data = request.session['discount']
            discount_percentage = Decimal(discount_data['percentage'])  # Convert to Decimal
            discounted_total = total * (1 - discount_percentage / 100)  # Apply discount

        context = {
            'cart_items_by_restaurant': cart_items_by_restaurant,
            'total': total,
            'discounted_total': discounted_total,  # Pass the discounted total to the template
        }
        return render(request, 'order/cart.html', context)
    else:
        # Redirect the user to login if they are not authenticated
        return redirect('login')

# users/views.py
def add_to_cart(request, item_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items to the cart.")
        return redirect('login')  # Redirect to the login page

    item = get_object_or_404(MenuItem, id=item_id)

    # Retrieve or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user, status='Active')

    # If multiple active carts exist, handle them
    active_carts = Cart.objects.filter(user=request.user, status='Active')
    if active_carts.count() > 1:
        # Merge all active carts into the first one
        main_cart = active_carts.first()
        for cart in active_carts[1:]:
            for cart_item in cart.items.all():
                # Check if the item already exists in the main cart
                existing_item = main_cart.items.filter(item=cart_item.item).first()
                if existing_item:
                    existing_item.quantity += cart_item.quantity
                    existing_item.save()
                else:
                    cart_item.cart = main_cart
                    cart_item.save()
            cart.delete()  # Delete the duplicate cart
        cart = main_cart

    # Check if the item is already in the cart
    cart_item = CartItem.objects.filter(cart=cart, item=item).first()

    if cart_item:
        # If the item is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If the item is not in the cart, create a new cart item
        CartItem.objects.create(cart=cart, item=item, quantity=1)

    return redirect('cart')  # Redirect to the cart page

def update_cart(request, item_id):
    # Get the cart item based on the user and item ID
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Update the cart item quantity
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, f"Updated quantity of {cart_item.item.name} to {cart_item.quantity}")
        else:
            messages.error(request, "Invalid quantity entered.")

    # Redirect back to the cart page
    return redirect('cart')


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Get the cart for the current user
            cart = Cart.objects.filter(user=request.user, status='Active').first()
            if cart:
                # Get the cart item to be removed
                cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
                cart_item.delete()  # Remove the cart item
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Cart not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the user's active cart
    cart = Cart.objects.filter(user=request.user).first()

    # Check if the cart exists and has items
    if not cart or cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate the total price of the items in the cart
    total_price = sum(item.total_price() for item in cart.items.all())

    # Apply discount if available
    discount = None
    if 'discount' in request.session:
        discount_data = request.session['discount']
        discount = Discount.objects.get(id=discount_data['id'])
        discount_percentage = Decimal(discount_data['percentage'])  # Convert to Decimal
        total_price *= (1 - discount_percentage / 100)  # Apply discount
        del request.session['discount']  # Clear the discount from the session

    # Create the order
    order = Order.objects.create(
        user=request.user,
        restaurant=cart.items.first().item.restaurant,
        status='Pending',
        total_price=total_price,
        discount=discount,  # Add the applied discount
    )

    # Transfer cart items to order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity
        )

    # Clear the cart after checkout
    cart.items.all().delete()

    # Redirect to the order confirmation page
    return redirect('order_confirmed', order_id=order.id)

def confirm_order(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the user's active cart
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or cart.items.count() == 0:
        return redirect('cart')  # If the cart is empty, redirect to cart page

    # Create a new order
    order = Order.objects.create(user=request.user, restaurant=cart.items.first().item.restaurant, status='Pending')

    # Transfer cart items to order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(order=order, item=cart_item.item, quantity=cart_item.quantity)

    # Clear the cart after checkout
    cart.items.all().delete()  # Or alternatively cart.delete() if you want to delete the whole cart

    # Redirect to the order confirmation page
    return redirect('order_confirmation', order_id=order.id)

def order_confirmed(request, order_id):
    # Fetch the order using the ID
    order = Order.objects.get(id=order_id)
    return render(request, 'order/confirmed.html', {'order': order})

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirects to the home page