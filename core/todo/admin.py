from django.contrib import admin
from .models import Task, Category, TaskComment
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_done', 'priority', 'due_date', 'created_at')
    list_filter = ('is_done', 'priority', 'due_date', 'user')
    search_fields = ('title', 'description', 'user__email')
    raw_id_fields = ('user', 'category')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__email')

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    search_fields = ('task__title', 'user__email', 'text')
