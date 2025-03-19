from django.urls import path
from django.contrib.auth.decorators import login_required
# from .views import show_task
from tasks.views import CreateTask, UpdateTask, DeleteTask, TaskDetail, CreateProject, UpdateProject, DeleteProject
urlpatterns = [
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    path('task/<task_id>/details', TaskDetail.as_view(), name='task-details'),
    path('delete-task/<task_id>', DeleteTask.as_view(), name='delete-task'),
    # path('create-project/', create_project, name='create-project'),
    path('create-project/', CreateProject.as_view(), name='create-project'),
    path('update-project/<int:id>', UpdateProject.as_view(), name='update-project'),
    path('delete-project/<int:id>', DeleteProject.as_view(), name='delete-project'),

]