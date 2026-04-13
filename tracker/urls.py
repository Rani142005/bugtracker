from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),

    path('add-bug/', views.add_bug, name='add_bug'),
    path('bugs/', views.bug_list, name='bug_list'),

    path('update-bug/<int:bug_id>/', views.update_bug, name='update_bug'),
    path('delete-bug/<int:bug_id>/', views.delete_bug, name='delete_bug'),
    path('delete-attachment/<int:attachment_id>/', views.delete_attachment, name='delete_attachment'),

    path('add-task/', views.add_task, name='add_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/toggle/', views.toggle_notification_read, name='toggle_notification_read'),
    path('notifications/mark-all/', views.mark_all_notifications, name='mark_all_notifications'),
    path('users/', views.users_view, name='users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/change-password/<int:user_id>/', views.change_user_password, name='change_user_password'),
    path('register/', views.register, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]