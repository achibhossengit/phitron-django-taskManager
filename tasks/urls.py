from django.urls import path
# from .views import show_task
from tasks.views import manager_dashboard, user_dashboard, dashboard, test_file, create_task, show_all_tasks
urlpatterns = [
    path('manager-dashboard', manager_dashboard),
    path('user-dashboard', user_dashboard),
    path('common-dashboard', dashboard),
    path('test', test_file),
    path('create-task', create_task),
    path('show-tasks', show_all_tasks)
]