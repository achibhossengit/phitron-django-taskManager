from django import forms
from tasks.models import Task, TaskDetail


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees',[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]

""" Mixins """
class StyledFormMixin:
    # MRO-> Method Resulation Order
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_default_classes()

    default_classes = 'border-2 focus:outline-none focus:border-blue-500 border-gray-200 focus:border-blue-500 rounded-md w-full p-3'

    def apply_default_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{self.default_classes} ',
                    'placeholder': f'Enter {field.label.lower()}',
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("inside date filed")
                field.widget.attrs.update({
                    'class': 'border-2 rounded-md my-5'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'mb-3'
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
    
class TaskModelForm(StyledFormMixin, forms.ModelForm):    
    class Meta:
        model = Task
        # fields = "__all__"
        fields = ["title", "description", "due_date", "assigned_to"]
        """ To define default widget """
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }


class TaskDetialModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes','asset']
    
