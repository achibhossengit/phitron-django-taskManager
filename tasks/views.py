from django.shortcuts import render
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import  Task, Employee, TaskDetail, Project
from django.http import HttpResponse
from django.db.models import Q, Count, Max, Min, Avg

# Create your views here.
def dashboard(request):
    return render(request, "dashboard/dashboard-common.html")

def manager_dashboard(request):
    tasks = Task.objects.all()

    # getting task count
    total_task = tasks.count()
    completed_task = Task.objects.filter(status='COMPLETED').count()
    in_progress = Task.objects.filter(status = 'IN_PROGRESS').count()
    pending_task = Task.objects.filter(status = 'PENDING').count()

    context = {
        'tasks': tasks,
        'total_task': total_task,
        'completed_task': completed_task,
        'in_progress': in_progress,
        'pending_task': pending_task
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
    employees = Employee.objects.all()
    form = TaskModelForm()
    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ for Model form """
            form.save()
            message = "Task added successfully!"
            return render(request, 'create_task.html', {'form': form, 'message': message})
    context = {'form':form}
    return render(request, 'create_task.html', context)

def show_all_tasks(request):
    """ Data Retrive (django aggregations)"""

    tasks = Task.objects.aggregate(net_task= Count('id'))
    projects = Project.objects.annotate(net_task=Count('tasks')).order_by('net_task')
    return render(request, 'show_tasks.html', {'tasks':tasks, 'projects':projects})
