from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
# custom model form 
class CustomRegisterForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    # field error
    def clean_password(self):
        password = self.cleaned_data.get('password')
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$"

        # it will raise single errors in one time
        # if len(password) < 8:
        #     raise forms.ValidationError("Password must be at least 8 character long")
        # if not re.fullmatch(pattern, password):
        #     raise forms.ValidationError("Password must include uppercase, lowercase, number & special character")

        # it will raise multiple errors in one time
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 character long")
        if not re.fullmatch(pattern, password):
            errors.append("Password must include uppercase, lowercase, number & special character")

        if errors:
            raise forms.ValidationError(errors)

        return password
    
    # non field error
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password did't match!")

        return cleaned_data # it will return all data from form.

        
    # field error for unique email
    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists(): # filter will return a queryset. but, exitsts will return True or false. 
            raise forms.ValidationError("This email address is already registered. Please try another.")
        
        return email
        
        
