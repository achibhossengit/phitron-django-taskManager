from django.shortcuts import render, redirect
from django.contrib.auth import logout, aauthenticate

# Create your views here.
def home(request):
    """when i use form without action """
    # if request.method == 'POST':
    #     logout(request)
    #     return redirect('sign-in')
    return render(request, 'home_page.html')