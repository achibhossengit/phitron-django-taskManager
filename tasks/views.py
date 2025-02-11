from django.shortcuts import render
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import  Task, Employee, TaskDetail, Project
from django.http import HttpResponse
from django.db.models import Q, Count, Max, Min, Avg

# Create your views here.
def dashboard(request):
    return render(request, "dashboard/dashboard-common.html")

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

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
