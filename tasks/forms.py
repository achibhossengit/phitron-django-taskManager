from django import forms
from tasks.models import Task


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees',[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


    
class TaskModelForm(forms.ModelForm):    
    class Meta:
        model = Task
        # fields = "__all__"
        fields = ["title", "description", "due_date", "assigned_to"]
        # exclude = ["project", "is_completed"]
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'border-2 rounded-md w-full'
            }),
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
            }