# restaurants/views.py
from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuItem

def home(request):
    featured_restaurants = Restaurant.objects.all()[:4]  # Fetch some restaurants or however you filter
    return render(request, 'home.html', {'featured_restaurants': featured_restaurants})

def restaurant_list(request):
    tag = request.GET.get('tag')
    if tag:
        restaurants = Restaurant.objects.filter(menu_items__dietary_tags__name=tag).distinct()
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'restaurants/restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})