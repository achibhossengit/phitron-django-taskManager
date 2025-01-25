from django.urls import path
# from .views import show_task
from tasks.views import show_task, show_specific_task, dashboard_rendaring
urlpatterns = [
    path('show-task', show_task),
    # dynamic urls
    path('show-task/<id>/', show_specific_task),
    path('dashboard', dashboard_rendaring)
]