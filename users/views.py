from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from orders.models import Order


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role (student or vendor)
        email = request.POST.get('email')  # Get the email address

        # Verify if email matches the role criteria (student or vendor)
        if not verify_role_based_on_email(role, email):
            return HttpResponse(f"Invalid email address for the selected role: {role}")

        # Use Django's machinery to attempt to see if the username/password combination is valid.
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))  # Redirect to the homepage (make sure 'index' is a valid URL pattern)
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login.")

    # If the request is not a HTTP POST, render the login form (HTTP GET)
    else:
        return render(request, 'registrations/login.html')

# Register page (Sign up)
def register(request):
    if request.method == 'POST':
        # Use Django's UserCreationForm to handle user creation
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # After registration, you might want to log the user in automatically
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('profile')  # Redirect to the profile page after successful registration
    else:
        form = UserCreationForm()  # Blank form if GET request

    return render(request, 'registrations/registration.html', {'form': form})


# Profile page (Shows user details and order history)
@login_required  # Only logged-in users can access this page
def profile(request):
    # Fetch the user's orders
    orders = Order.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {'orders': orders})


def verify_role_based_on_email(role, email):
    """
    Verifies whether the email corresponds to the selected role (student or vendor).
    """
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

