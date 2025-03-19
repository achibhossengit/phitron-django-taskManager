from django.urls import path
from django.contrib.auth.decorators import login_required
# from .views import show_task
from tasks.views import create_project, CreateTask, UpdateTask, DeleteTask, ShowProjects, TaskDetail
urlpatterns = [
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    path('task/<task_id>/details', TaskDetail.as_view(), name='task-details'),
    path('delete-task/<task_id>', DeleteTask.as_view(), name='delete-task'),
    path('create-project/', create_project, name='create-project'),
    path('show-projects/', ShowProjects.as_view(), name='show-projects'),
]