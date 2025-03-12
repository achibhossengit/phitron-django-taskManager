from django.urls import path
from django.contrib.auth.decorators import login_required
# from .views import show_task
from tasks.views import manager_dashboard, employee_dashboard, create_task, show_all_tasks, update_task, delete_task, task_details, Greatings, HiGreatings, CreateTask, create_project
urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', employee_dashboard),
    # path('create-task/', login_required(CreateTask.as_view()), name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('create-project/', create_project, name='create-project'),
    path('show-tasks/', show_all_tasks),
    path('task/<task_id>/details', task_details, name='task-details'),
    path('update-task/<int:id>/', update_task, name='update-task'),
    path('delete/-task/<int:id>', delete_task, name='delete-task'),

    path('greatings', HiGreatings.as_view(greatings = 'How are you today?'), name='greatings')
]