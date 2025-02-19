from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users.forms import RegisterForm, CustomRegisterForm
from django.contrib import messages


def sign_up(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    elif request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # confirm_password = form.cleaned_data.get('password2')
            # if password == confirm_password:
            #     User.objects.create(username= username, password=password)
            # else:
            #     print("Password aren't same!")
        # else:
        #     print("form is invalid!")

            form.save()
            messages.success(request, 'User Added Successfully!')
        
    return render(request, 'register/sign_up.html', {'form': form})

def sign_in(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "user not found")
            print('invalid user')
            return redirect('sign-in')

    return render(request, 'register/sign_in.html') # for get request


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        # return render(request, 'register/sign_in.html') #render: টেমপ্লেট রেন্ডার করে in old url।
        return redirect('sign-in') # redirect: নতুন URL-এ পুনঃনির্দেশ করে।
    else:
        return render(request, 'home_page.html')