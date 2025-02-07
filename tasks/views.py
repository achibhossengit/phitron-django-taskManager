from django.shortcuts import render
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import  Task, Employee, TaskDetail
from django.http import HttpResponse
from django.db.models import Q

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
    # print(employees)
    # form = TaskForm(employees = employees)
    form = TaskModelForm()
    if request.method == 'POST':
        # form = TaskForm(request.POST, employees = employees)
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ for Model form """
            form.save()

            message = "Task added successfully!"
            return render(request, 'create_task.html', {'form': form, 'message': message})

            """ for Django Form data"""
            # data = form.cleaned_data # here, data is a dictionary
            # title = data.get('title') # get: to access dictionary data, if dictionary have't title key, its return none
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to') # here, is a many to many relations

            # task = Task.objects.create(title=title, description = description, due_date=due_date)
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task added successfully!")

    context = {'form':form}
    return render(request, 'create_task.html', context)

def show_all_tasks(request):
    """ Data Retrive """
    # tasks = Task.objects.all()
    # task_2 = Task.objects.get(id=2)
    # first_task = Task.objects.first()
    # # get can't return more than one objects thats why
    # pending_tasks = Task.objects.filter(status="PENDING")
    # not_low_task = TaskDetail.objects.exclude(priority = 'L')
    # return render(request, 'show_tasks.html', {'tasks': tasks, 'task2': task_2, 'first_task':first_task, 'pending_tasks': pending_tasks, 'not_low_tasks':not_low_task})
    
    # search_word = "t"
    # search_and = Task.objects.filter(title__icontains=search_word, status= 'PENDING')
    # search_or = Task.objects.filter(Q(status='PENDING') | Q(status='IN_PROGRESS'))
    # return render(request, 'show_tasks.html', {'and_tasks': search_and, 'or_tasks': search_or})

    # filter can return a empty query set
    is_exits = Task.objects.filter(status= 'khjhjhsdf').exists()
    return render (request, 'show_tasks.html', {'is_exits': is_exits})