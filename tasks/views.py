from django.shortcuts import render, redirect
from tasks.forms import TaskForm, TaskModelForm, TaskDetialModelForm
from tasks.models import  Task, Project
from django.http import HttpResponse
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# checking function
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()


# All views
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
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test_file(request):
    context = {
        "names": ['Al Mahmud', 'Appolo', 'Taniya', 'Sweety'],
        "age": 23
    }
    return render(request, 'test.html', context)


@login_required(login_url='sign-in')
@permission_required(perm='tasks.add_task' ,login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetialModelForm()
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetialModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ for Model form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail_form.save()

            messages.success(request, "Task added successfully!")
            return redirect('create-task')
    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form
        }
    return render(request, 'create_task.html', context)

@login_required()
@permission_required(perm='tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    task_detail_form = TaskDetialModelForm(instance = task.details)

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetialModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ for Model form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail_form.save()

            messages.success(request, "Task updated successfully!")
            return redirect('update-task', id)
    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form
        }
    return render(request, 'create_task.html', context)

@login_required()
@permission_required(perm='tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted Successfully!")
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong!')
        return redirect('manager-dashboard')

@login_required()
@permission_required(perm='tasks.view_task', login_url='no-permission')
def show_all_tasks(request):
    """ Data Retrive (django aggregations)"""
    tasks = Task.objects.aggregate(net_task= Count('id'))
    projects = Project.objects.annotate(net_task=Count('tasks')).order_by('net_task')
    return render(request, 'show_tasks.html', {'tasks':tasks, 'projects':projects})

@login_required()
@permission_required(perm='tasks.view_task', login_url='no-permission')
def show_task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'task_details.html', {'task': task})