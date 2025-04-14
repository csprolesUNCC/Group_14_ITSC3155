from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Replace with your actual dashboard route name
        else:
            return render(request, 'base/login.html', {'error': 'Invalid credentials'})

    return render(request, 'base/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            return render(request, 'base/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'base/signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')  # Or change to your actual dashboard route

    return render(request, 'base/signup.html')