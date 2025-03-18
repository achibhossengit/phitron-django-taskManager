from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_img')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )

    # to add some extra fileds in admin panel. "edit/change" is not working here. for edit/change you have to use fieldsets
    # add_fieldsets = (
        # (),
    # )

    list_display = ('username', 'email', 'first_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-username',)
    