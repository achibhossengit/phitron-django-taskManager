from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label='Task Title')
    description = forms.CharField(
        label='Task Descriptions',
        widget=forms.Textarea
    )
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(
        widget= forms.CheckboxSelectMultiple,
        choices=[] , 
        label="Assigned To"
        )

    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees", [])
        # print(args, kwargs)
        # print(employees)
        super().__init__(*args, **kwargs)
        # print("Pointer is here:",self.fields['assigned_to'])
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees
        ]