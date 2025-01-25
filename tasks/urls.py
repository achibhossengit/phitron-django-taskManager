from django.urls import path
# from .views import show_task
from tasks.views import dashboard_rendaring
urlpatterns = [
    path('dashboard', dashboard_rendaring)
]