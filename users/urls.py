from django.urls import path
from users.views import dashboard, assign_role, CustomLoginView, ProfileView, ChangePassword, CustomPasswordReset, CustomPasswordResetConfirmView, EditProfileView, SignUp, ActiveUserView, CreateGroup, AssignRole
from core.views import home
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('', home, name='home'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(template_name="register/sign_in.html"), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>', ActiveUserView.as_view()),
    # path('admin/<int:user_id>/assign-role/ ', assign_role, name='assign-role'),
    path('admin/<int:user_id>/assign-role/ ', AssignRole.as_view(), name='assign-role'),
    path('admin/create-group', CreateGroup.as_view(), name='create-group'),
    path('profile/', ProfileView.as_view(), name= 'profile'),
    path('change-password', ChangePassword.as_view(), name= 'change-password'),
    path('password-changed/done', PasswordChangeDoneView.as_view(template_name = 'accounts/password_done.html'), name='password_change_done'),
    path('password-reset', CustomPasswordReset.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile', EditProfileView.as_view(), name='edit-profile'),
]
