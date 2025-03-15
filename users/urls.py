from django.urls import path
from users.views import sign_up, sign_in, sign_out, active_user, admin_dashboard, manager_dashboard, employee_dashboard, assign_role, create_group, group_list, CustomLoginView, ProfileView
from core.views import home
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard'),
    path('sign-up/', sign_up, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(template_name="register/sign_in.html"), name='sign-in'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('', home, name='home'),
    path('activate/<int:user_id>/<str:token>', active_user),
    path('admin/<int:user_id>/assign-role/ ', assign_role, name='assign-role'),
    path('admin/create-group', create_group, name='create-group'),
    path('admin/group-list', group_list, name= 'group-list'),
    path('profile/', ProfileView.as_view(), name= 'profile'),
]
