from django.urls import path
# from .views import show_task
from tasks.views import manager_dashboard, user_dashboard, dashboard, test_file, input_form
urlpatterns = [
    path('manager-dashboard', manager_dashboard),
    path('user-dashboard', user_dashboard),
    path('common-dashboard', dashboard),
    path('test', test_file),
    path('input_form', input_form)
]