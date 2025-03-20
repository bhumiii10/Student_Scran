# restaurants/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem
from .models import Restaurant, Review
from .forms import ReviewForm
from django.contrib import messages
from restaurants.models import Discount


def apply_discount(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')

        try:
            discount = Discount.objects.get(code=discount_code, is_active=True)
            # Store the discount in the session
            request.session['discount'] = {
                'id': discount.id,
                'code': discount.code,
                'percentage': float(discount.discount_percentage),
            }
            messages.success(request, f"Discount code '{discount.code}' applied successfully!")
        except Discount.DoesNotExist:
            messages.error(request, "Invalid or expired discount code.")
            if 'discount' in request.session:
                del request.session['discount']  # Clear any invalid discount

        return redirect('cart')

def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ReviewForm()
    return render(request, 'restaurants/add_review.html', {'form': form, 'restaurant': restaurant})


def home(request):
    featured_restaurants = Restaurant.objects.all()[:4]  # Fetch some restaurants or however you filter
    return render(request, 'home.html', {'featured_restaurants': featured_restaurants})

def restaurant_list(request):
    search_query = request.GET.get('search', '')
    tag = request.GET.get('tag')
    if tag:
        restaurants = Restaurant.objects.filter(menu_items__dietary_tags__name=tag).distinct()
    else:
        restaurants = Restaurant.objects.all()

        # Now, filter by search query for restaurant name
    if search_query:
        restaurants = restaurants.filter(name__icontains=search_query)  # Case-insensitive search

    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'restaurants/restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})

