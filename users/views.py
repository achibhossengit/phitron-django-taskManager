from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group
from users.forms import CustomRegisterForm, CustomLoginForm, AssignRoleForm, CreateGroupForm, CustomChangePasswordForm, PasswordReset, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Prefetch
from tasks.models import Task, Project
from django.db.models import Q, Count
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import date
from django.views import View
User = CustomUser


# checking function
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

def dashboard(request):
    type = request.GET.get('type', 'all')
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    if is_admin(request.user):
        users = None
        tasks = None
        projects = None
        groups = None
        if type == 'all':
            tasks = base_query.all()
            title = 'All Tasks'
        elif type == 'users':
            users = User.objects.prefetch_related( 
                Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
            for user in users:
                if user.all_groups:
                    user.group_name = user.all_groups[0].name
                else:
                    user.group_name = 'No Group Assigned'
            title = 'All of Your Users'
        elif type == 'projects':
            projects = Project.objects.all()
            title = 'Projects'
        elif type == 'groups':
            groups = Group.objects.all()
            title = 'Groups And Permissions'

        context = {
            'tasks': tasks,
            'users': users,
            'projects': projects,
            'groups': groups,
            'title': title
        }
        return render(request, 'dashboard/admin-dashboard.html', context)
    
    elif is_manager(request.user):
        # getting task count
        counts = Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
            
            )
        # Retriving task data
        projects = None
        tasks = None
       
        if type == 'completed':
            tasks = base_query.filter(status='COMPLETED')
            title = 'Completed Tasks'
        elif type == 'in_progress':
            tasks = base_query.filter(status='IN_PROGRESS')
            title = 'In Progress Tasks'
        elif type == 'pending':
            tasks = base_query.filter(status='PENDING')
            title = 'Pending Tasks'
        elif type == 'projects':
            projects = Project.objects.all()
            title = 'Projects'
        else:
            tasks = base_query.all()
            title = 'All Tasks'

        context = {
            'tasks': tasks,
            'counts': counts,
            'projects': projects,
            'title': title,
        }
        return render(request, "dashboard/manager-dashboard.html", context)
    
    elif is_employee(request.user):
        tasks = request.user.tasks.all()
        today_tasks = tasks.filter(due_date=date.today())
        context = {'tasks': tasks, 'today_tasks': today_tasks}
        return render(request, "dashboard/employee-dashboard.html", context)


class SignUp(CreateView):
    model = CustomUser
    form_class = CustomRegisterForm
    pk_url_kwarg = 'id'
    template_name = 'register/sign_up.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password')) # hashing
        user.is_active = False
        self.object = user.save()
        return super().form_valid(form)
            

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

# Logout view in urls

class ActiveUserView(View):
    def get(self, request, user_id, token):
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
            return redirect('dashboard')
    return render(request, 'admin/assign_role.html', {'form': form})

class AssignRole(View):
    def get(self, request, user_id):
        form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {'form': form})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            user.save()
            messages.success(request, f"{user.username} has been assigned to {role.name} role")
            return redirect('dashboard')
        

class CreateGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'group.add_group'
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('dashboard')
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        messages.success(request, "Groups Created Successfully!")
        return super().post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['bio'] = user.bio
        context['profile_img'] = user.profile_img.url
        context['role'] = user.groups.first().name
        return context
        

class ChangePassword(PasswordChangeView):
    template_name = "accounts/change_password.html"
    form_class = CustomChangePasswordForm # ChangePasswordDoneView is located in users.url


class CustomPasswordReset(PasswordResetView):
    form_class = PasswordReset
    template_name = 'register/password_reset.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'register/reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, "An Email was sent your email. Please check your Email Inbox.")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'register/password_reset.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Password Reset Successfully!")
        return super().form_valid(form)
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/update_form.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    

    def form_valid(self, form):
        form.save()
        return redirect('profile')
