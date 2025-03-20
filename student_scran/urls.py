"""
URL configuration for student_scran project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from users import views
from restaurants.views import home, restaurant_list, restaurant_detail, add_review, apply_discount
# student_scran/urls.py
from django.contrib import admin
from django.urls import path, include
from restaurants.views import home, restaurant_list, restaurant_detail  # Import from restaurants app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('cart/', views.cart_view, name='cart'),  # Cart page
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('order_confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('restaurants/<int:restaurant_id>/add_review/', add_review, name='add_review'),
    path('apply_discount/', apply_discount, name='apply_discount'),


]

