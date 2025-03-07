
# Login page which includes user to select if they are a vendor or student
# rango/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role (student or vendor)
        email = request.POST.get('email')  # Get the email address

        # Verify if email matches the role criteria (student or vendor)
        if not verify_role_based_on_email(role, email):
            return HttpResponse("Invalid email address for the selected role: {role}")

        # Use Django's machinery to attempt to see if the username/password combination is valid.
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))  # Redirect to the homepage
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login.")

    # If the request is not a HTTP POST, render the login form (HTTP GET)
    else:
        return render(request, 'rango/login.html')


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


