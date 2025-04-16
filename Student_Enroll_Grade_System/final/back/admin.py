from django.contrib import admin
from .models import newuser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = newuser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_teacher')
    list_filter = ('is_staff', 'is_active', 'is_teacher')
    fieldsets = (
        (None, {'fields': ('username', 'password')}), #default
        ('Personal info', {'fields': ('email',)}), #info 
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_teacher')}), #permission
    )    # user info page

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_teacher')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    search_fields = ('email', 'username')
    ordering = ('username',)
admin.site.register(newuser, CustomUserAdmin)