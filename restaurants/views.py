from django.shortcuts import render
from restaurants.models import Restaurant

def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants.html', {'restaurants': restaurants})

def home(request):
    return render(request, 'home.html')