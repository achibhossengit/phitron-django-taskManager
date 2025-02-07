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

""" Mixins """
class StyledFormMixin:
    # MRO-> Method Resulation Order
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.apply_default_classes()

    default_classes = 'border-2 rounded-md w-full p-3 my-5'

    def apply_default_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{self.default_classes} ',
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("inside date filed")
                field.widget.attrs.update({
                    'class': 'border-2 rounded-md my-5'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # print("inside assigned to")
                field.widget.attrs.update({
                    'class': 'my-5'
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

        # exclude = ["project", "is_completed"]

        # """ Manual Widget """
        # widgets = {
        #     'title':forms.TextInput(attrs={
        #         'class':'border-2 rounded-md w-full p-3 my-5',
        #         'placeholder': 'Enter task title'
        #     }),
        #     'description':forms.Textarea(attrs={
        #         'class':'border-2 rounded-md w-full p-3 my-5',
        #         'placeholder': 'Define your task'
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class':'border-2 rounded-md my-5'
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class':'  my-5',
        #     })
        #     }

    """ Widget using Mixin """

    # MRO: TaskModelForm -> StyleFormMixin -> ModelForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_default_classes()

