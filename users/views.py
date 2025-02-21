from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users.forms import RegisterForm, CustomRegisterForm
from django.contrib import messages


def sign_up(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
        return render(request, 'register/sign_up.html', {'form': form})
    elif request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('user:', user)
            user.set_password(form.cleaned_data.get('password')) # for hasing
            user.is_active = False
            user.save()
            messages.success(request, 'User Added Successfully! Please check your email for log in.')
            return redirect('sign-in')
        else:
            print('Form Validation error')
            return render(request, 'register/sign_up.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm(data = request.POST)
    if request.method=='POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'register/sign_in.html', {'form': form}) # for get request


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        # return render(request, 'register/sign_in.html') #render: টেমপ্লেট রেন্ডার করে in old url।
        return redirect('sign-in') # redirect: নতুন URL-এ পুনঃনির্দেশ করে।
    else:
        return render(request, 'home_page.html')