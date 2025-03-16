from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from users.forms import RegisterForm, CustomRegisterForm, CustomLoginForm, AssignRoleForm, CreateGroupForm, CustomChangePasswordForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from tasks.models import Task
from django.db.models import Q, Count
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView



# checking function
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            # user.group_name = user.groups.first().name
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type', 'all')
    
    # getting task count
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
        
        )
    # Retriving task data
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    if type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    if type == 'pending':
        tasks = base_query.filter(status='PENDING')
    if type == 'all':
        tasks = base_query.all()

    context = {
        'tasks': tasks,
        'counts': counts
    }
    print(request.user.username)
    print(request.user.groups.first().name)
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/employee-dashboard.html")



def sign_up(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
        return render(request, 'register/sign_up.html', {'form': form})
    elif request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # print('user:', user)
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

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

@login_required(login_url='sign-in')
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        # return render(request, 'register/sign_in.html') #render: টেমপ্লেট রেন্ডার করে in old url।
        return redirect('home') # redirect: নতুন URL-এ পুনঃনির্দেশ করে।
    
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
    
@user_passes_test(is_admin, login_url='no-permission')
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

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} Group created successfully!")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form':form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    
    return render(request, 'admin/group_list.html', {'groups': groups})

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
        

class ChangePassword(PasswordChangeView):
    template_name = "accounts/change_password.html"
    form_class = CustomChangePasswordForm
