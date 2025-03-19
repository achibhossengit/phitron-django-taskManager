from django.urls import path
from users.views import sign_up, sign_in, sign_out, active_user, dashboard, assign_role, create_group, group_list, CustomLoginView, ProfileView, ChangePassword, CustomPasswordReset, CustomPasswordResetConfirmView, EditProfileView
from core.views import home
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
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
    path('change-password', ChangePassword.as_view(), name= 'change-password'),
    path('password-changed/done', PasswordChangeDoneView.as_view(template_name = 'accounts/password_done.html'), name='password_change_done'),
    path('password-reset', CustomPasswordReset.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile', EditProfileView.as_view(), name='edit-profile'),
]
