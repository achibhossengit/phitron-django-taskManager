from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employee, Task

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
    employees = Employee.objects.all() # fetch employee data from database
    # for get method
    form = TaskForm(employees = employees) # form initilization

    if request.method == 'POST':
        form = TaskForm(request.POST, employees = employees)
        if form.is_valid():
            # print(form.cleaned_data)
            data = form.cleaned_data
            title = data.get('title')
            description = data['description']
            due_date = data['due_date']
            assigned_to = data['assigned_to'] # it will a list of employees

            task = Task.objects.create(title=title, description=description, due_date=due_date)
            # here, assigned_to variable contain some id of employees. but, our hidden assigned field of task table receive an object of employee. so,
            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)

            return HttpResponse("Task added successfully!!")

    context = {"form_a": form}
    return render(request, "form.html", context)