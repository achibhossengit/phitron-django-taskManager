from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegisterForm
from django.contrib import messages


def sign_up(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    elif request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # confirm_password = form.cleaned_data.get('password2')
            # if password == confirm_password:
            #     User.objects.create(username= username, password=password)
            # else:
            #     print("Password aren't same!")
        # else:
        #     print("form is invalid!")

            form.save()
            messages.success(request, 'User Added Successfully!')
        
    return render(request, 'register/sign_up.html', {'form': form})
