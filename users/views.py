from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from users.forms import RegisterForm, CustomRegisterForm, CustomLoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

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
    form = CustomLoginForm()
    if request.method=='POST':
        form = CustomLoginForm(data = request.POST)
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
    
def active_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid token or user id!')
    except User.DoesNotExist:
        return HttpResponse('User not found')
    
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method=='POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            user.save()
            messages.success(request, f"{user.username} has been assigned to {role.name} role")
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form})

def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} Group created successfully!")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form':form})
        