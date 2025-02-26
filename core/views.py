from django.shortcuts import render, redirect
from django.contrib.auth import logout, aauthenticate

# Create your views here.
def home(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    return render(request, 'home.html')

def no_permission(request):
    return render(request, 'no_permission.html')