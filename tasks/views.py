from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request): #here home is a view
    return HttpResponse("Wellcome to task management system!")

def contact(request):
    return HttpResponse("<h1 style='color: green; background-color:red'>This is contact page of mine website!<h1>")

def show_task(request):
    return HttpResponse("This page is all about show task.")

def show_specific_task(request, id):
    print(type(id))
    return HttpResponse(f"This is task: {id}")


def dashboard_rendaring(request):
    return render(request, "dashboard.html")