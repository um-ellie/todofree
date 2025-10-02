from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User,Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    inlines = (ProfileInline,)
    list_display = ("email","is_superuser","is_staff","is_active","created_at")
    list_filter = ("is_staff","is_active")
    ordering = ("email",)
    search_fields = ("email",)
    readonly_fields = ("created_at","updated_at")

    fieldsets = (
        (_('Authentication'), {"fields": ("email","password")}),
        (_('Permissions'), {"fields": ("is_active","is_staff","is_superuser","groups","user_permissions")}),
        (_('Important dates'), {"fields": ("last_login","created_at","updated_at")})
    )

    add_fieldsets = (
        (_("Registration"), {
            "classes":("wide",),
            "fields": ("email","password1","password2","is_active","is_staff","is_superuser"),
        }),
    )


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ("user","first_name","last_name","created_at")
#     search_fields = ("user__email","first_name","last_name")



