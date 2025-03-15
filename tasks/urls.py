from django.urls import path
from django.contrib.auth.decorators import login_required
# from .views import show_task
from tasks.views import create_task, show_projects, update_task, delete_task, task_details, CreateTask, create_project, UpdateTask, ShowProjects, TaskDetail
urlpatterns = [
    # path('create-task/', login_required(CreateTask.as_view()), name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('create-project/', create_project, name='create-project'),
    # path('show-projects/', show_projects, name='show-projects'),
    path('show-projects/', ShowProjects.as_view(), name='show-projects'),
    # path('task/<task_id>/details', task_details, name='task-details'),
    path('task/<task_id>/details', TaskDetail.as_view(), name='task-details'),
    # path('update-task/<int:id>/', update_task, name='update-task'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    path('delete/-task/<int:id>', delete_task, name='delete-task'),
]