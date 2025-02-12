from django.shortcuts import render, redirect
from tasks.forms import TaskForm, TaskModelForm, TaskDetialModelForm
from tasks.models import  Task, Employee, TaskDetail, Project
from django.http import HttpResponse
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

# Create your views here.
def dashboard(request):
    return render(request, "dashboard/dashboard-common.html")

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

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test_file(request):
    context = {
        "names": ['Al Mahmud', 'Appolo', 'Taniya', 'Sweety'],
        "age": 23
    }
    return render(request, 'test.html', context)


def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetialModelForm()
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetialModelForm(request.POST)
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

def show_all_tasks(request):
    """ Data Retrive (django aggregations)"""

    tasks = Task.objects.aggregate(net_task= Count('id'))
    projects = Project.objects.annotate(net_task=Count('tasks')).order_by('net_task')
    return render(request, 'show_tasks.html', {'tasks':tasks, 'projects':projects})
