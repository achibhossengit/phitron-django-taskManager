from django.shortcuts import render, redirect
from tasks.forms import TaskModelForm, TaskDetialModelForm, ProjectModelForm
from tasks.models import  Task, Project
from django.http import HttpResponse
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, ContextMixin, View):
    permission_required = 'tasks.add_task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskModelForm()
        context['task_detail_form'] = TaskDetialModelForm()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'form.html', context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetialModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ for Model form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail_form.save()

            messages.success(request, "Task added successfully!")
            context =  self.get_context_data()
            return render(request, 'form.html', context)

class UpdateTask(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'tasks.change_task'
    model = Task
    form_class = TaskModelForm # if none: its make a form of provided model
    template_name = 'form.html'
    context_object_name = 'task' # create a object of 'Task' and passed it as a context using 'task'(bydefault) 
    pk_url_kwarg = 'id'
    
    # this view bydefault taken one view. but we need an another view to update taskdetail also
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form() # by default UpdateView pass form in context with using "form" named
        context['task_detail_form'] = TaskDetialModelForm(instance = self.get_object().details)
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetialModelForm(request.POST, request.FILES, instance=getattr(task, 'details', None))
        if task_form.is_valid() and task_detail_form.is_valid():
            task_form.save()
            task_detail_form.save()
            messages.success(request, "Task updated successfully")
            return redirect('manager-dashboard')
        else:
            return redirect('update-task', self.object.id)
    

        
class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'tasks.delete_task'
    model = Task
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('manager-dashboard')

class TaskDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'tasks.view_task'
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_options'] = Task.STATUS_OPTIONS
        return context
    
    def post(self, request ,*args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        print(selected_status)
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

    

def create_project(request):
    project_form = ProjectModelForm()
    if request.method == 'POST':
        project_form = ProjectModelForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            print('projcet creation done')
        else:
            print('validations failed')
    return render(request, 'form.html', {'project_form':project_form})


class ShowProjects(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_projects.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(net_task=Count('tasks')).order_by('net_task')
        return queryset