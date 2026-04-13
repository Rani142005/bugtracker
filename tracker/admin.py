from django.contrib import admin
from .models import Bug, Task


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'assigned_to')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('title', 'description')

