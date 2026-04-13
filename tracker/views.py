from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
import os

from .models import Bug, Task, BugComment, TaskComment, BugAttachment, Notification


def is_admin(user):
    return user.is_superuser


def notify_user(recipient, actor, message, bug=None, task=None):
    if recipient:
        Notification.objects.create(
            recipient=recipient,
            actor=actor,
            message=message,
            bug=bug,
            task=task,
        )


def register(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists'
            return render(request, 'register.html', {'error_message': error_message})

        User.objects.create_user(username=username, password=password)
        return redirect('/?registered=1')

    return render(request, 'register.html', {'error_message': error_message})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_superuser else 'dashboard')

    error_message = ''
    success_message = 'Account created successfully' if request.GET.get('registered') == '1' else ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard' if user.is_superuser else 'dashboard')

        error_message = 'Invalid username or password'

    return render(request, 'login.html', {'error_message': error_message, 'success_message': success_message})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_superuser:
        bugs = Bug.objects.all()
        tasks = Task.objects.all()
        notifications = Notification.objects.all()
    else:
        bugs = Bug.objects.filter(assigned_to=request.user)
        tasks = Task.objects.filter(assigned_to=request.user)
        notifications = Notification.objects.filter(recipient=request.user)

    today = timezone.localdate()
    overdue_tasks = tasks.filter(due_date__lt=today).exclude(status='Done')
    todays_workload = tasks.filter(due_date=today)

    context = {
        'total_bugs': bugs.count(),
        'open_bugs': bugs.filter(status='Open').count(),
        'closed_bugs': bugs.filter(status='Closed').count(),
        'tasks': tasks.count(),
        'overdue_tasks_count': overdue_tasks.count(),
        'todays_workload_count': todays_workload.count(),
        'unread_notifications_count_dashboard': notifications.filter(is_read=False).count(),
    }
    return render(request, 'dashboard.html', context)


from django.contrib.auth import get_user_model
import os

@user_passes_test(is_admin)
def admin_dashboard(request):

    today = timezone.localdate()
    tasks = Task.objects.all()
    notifications = Notification.objects.all()

    context = {
        'total_bugs': Bug.objects.count(),
        'open_bugs': Bug.objects.filter(status='Open').count(),
        'closed_bugs': Bug.objects.filter(status='Closed').count(),
        'tasks': tasks.count(),
        'overdue_tasks_count': tasks.filter(
            due_date__isnull=False,
            due_date__lt=today
        ).exclude(status='Done').count(),
        'todays_workload_count': tasks.filter(
            due_date__isnull=False,
            due_date=today
        ).exclude(status='Done').count(),
        'unread_notifications_count_dashboard': notifications.filter(is_read=False).count(),
    }

    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_admin)
def add_bug(request):
    users = User.objects.all()

    if request.method == 'POST':
        assigned_user = get_object_or_404(User, id=request.POST.get('assigned_to'))
        bug = Bug.objects.create(
            title=request.POST.get('title', '').strip(),
            description=request.POST.get('description', '').strip(),
            priority=request.POST.get('priority', 'Medium'),
            status=request.POST.get('status', 'Open'),
            severity=request.POST.get('severity', 'Minor'),
            assigned_to=assigned_user,
        )

        for uploaded_file in request.FILES.getlist('attachments'):
            BugAttachment.objects.create(
                bug=bug,
                file=uploaded_file,
                file_name=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type=uploaded_file.content_type or 'unknown',
                uploaded_by=request.user,
            )

        notify_user(
            recipient=assigned_user,
            actor=request.user,
            message=f'New bug assigned: {bug.title}',
            bug=bug,
        )
        return redirect('bug_list')

    return render(request, 'add_bug.html', {'users': users})


@login_required
def bug_list(request):
    if request.user.is_superuser:
        bugs = Bug.objects.all()
    else:
        bugs = Bug.objects.filter(assigned_to=request.user)

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    assigned_to = request.GET.get('assigned_to', '').strip()

    if query:
        bugs = bugs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(assigned_to__username__icontains=query)
        )

    if status:
        bugs = bugs.filter(status=status)

    if priority:
        bugs = bugs.filter(priority=priority)

    if request.user.is_superuser and assigned_to:
        bugs = bugs.filter(assigned_to_id=assigned_to)

    bugs = bugs.order_by('-updated_at')
    paginator = Paginator(bugs, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(
        request,
        'bug_list.html',
        {
            'bugs': page_obj.object_list,
            'page_obj': page_obj,
            'query': query,
            'status': status,
            'priority': priority,
            'assigned_to': assigned_to,
            'query_params': query_params.urlencode(),
            'status_choices': ['Open', 'In Progress', 'Closed'],
            'priority_choices': ['Low', 'Medium', 'High'],
            'users': User.objects.all() if request.user.is_superuser else [request.user],
        },
    )


@login_required
def update_bug(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)

    if not request.user.is_superuser and bug.assigned_to != request.user:
        messages.error(request, 'You are not allowed to update this bug')
        return redirect('bug_list')

    if request.method == 'POST':
        action = request.POST.get('action', 'update_status')

        if action == 'update_status':
            bug.status = request.POST['status']
            bug.save()
            notify_user(
                recipient=bug.assigned_to,
                actor=request.user,
                message=f'Bug status updated: {bug.title} -> {bug.status}',
                bug=bug,
            )
            messages.success(request, 'Bug status updated')
            return redirect('update_bug', bug_id=bug.id)

        if action == 'add_comment':
            content = request.POST.get('content', '').strip()
            if content:
                BugComment.objects.create(bug=bug, author=request.user, content=content)
                notify_user(
                    recipient=bug.assigned_to,
                    actor=request.user,
                    message=f'New comment on bug: {bug.title}',
                    bug=bug,
                )
            return redirect('update_bug', bug_id=bug.id)

        if action == 'add_attachment':
            uploaded_file = request.FILES.get('attachment')
            if uploaded_file:
                BugAttachment.objects.create(
                    bug=bug,
                    file=uploaded_file,
                    file_name=uploaded_file.name,
                    file_size=uploaded_file.size,
                    file_type=uploaded_file.content_type or 'unknown',
                    uploaded_by=request.user,
                )
                notify_user(
                    recipient=bug.assigned_to,
                    actor=request.user,
                    message=f'New attachment added to bug: {bug.title}',
                    bug=bug,
                )
            return redirect('update_bug', bug_id=bug.id)

    return render(
        request,
        'update_bug.html',
        {
            'bug': bug,
            'comments': bug.comments.select_related('author').all(),
            'attachments': bug.attachments.select_related('uploaded_by').all(),
            'status_choices': ['Open', 'In Progress', 'Closed'],
        },
    )


@user_passes_test(is_admin)
def delete_bug(request, bug_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid delete request.')
        return redirect('bug_list')

    bug = get_object_or_404(Bug, id=bug_id)
    bug.delete()
    messages.success(request, 'Bug deleted successfully.')
    return redirect('bug_list')


@user_passes_test(is_admin)
def delete_attachment(request, attachment_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid delete request.')
        return redirect('bug_list')

    attachment = get_object_or_404(BugAttachment, id=attachment_id)
    if attachment.file:
        attachment.file.delete(save=False)
    attachment.delete()
    messages.success(request, 'Attachment deleted successfully.')
    return redirect('update_bug', bug_id=request.POST.get('bug_id') or attachment.bug_id)


@user_passes_test(is_admin)
def add_task(request):
    users = User.objects.all()

    if request.method == 'POST':
        assigned_user = get_object_or_404(User, id=request.POST.get('assigned_to'))
        task = Task.objects.create(
            title=request.POST.get('title', '').strip(),
            description=request.POST.get('description', '').strip(),
            status=request.POST.get('status', 'Pending'),
            due_date=request.POST.get('due_date') or None,
            assigned_to=assigned_user,
        )
        notify_user(
            recipient=assigned_user,
            actor=request.user,
            message=f'New task assigned: {task.title}',
            task=task,
        )
        return redirect('task_list')

    return render(request, 'add_task.html', {'users': users})


@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    assigned_to = request.GET.get('assigned_to', '').strip()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(assigned_to__username__icontains=query)
        )

    if status:
        tasks = tasks.filter(status=status)

    if request.user.is_superuser and assigned_to:
        tasks = tasks.filter(assigned_to_id=assigned_to)

    tasks = tasks.order_by('-updated_at')
    paginator = Paginator(tasks, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(
        request,
        'task_list.html',
        {
            'tasks': page_obj.object_list,
            'page_obj': page_obj,
            'query': query,
            'status': status,
            'assigned_to': assigned_to,
            'query_params': query_params.urlencode(),
            'status_choices': ['Pending', 'In Progress', 'Done'],
            'users': User.objects.all() if request.user.is_superuser else [request.user],
        },
    )


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser and task.assigned_to != request.user:
        messages.error(request, 'You are not allowed to update this task')
        return redirect('task_list')

    if request.method == 'POST':
        action = request.POST.get('action', 'update_status')

        if action == 'update_status':
            task.status = request.POST.get('status', task.status)
            task.save()
            notify_user(
                recipient=task.assigned_to,
                actor=request.user,
                message=f'Task status updated: {task.title} -> {task.status}',
                task=task,
            )
            messages.success(request, 'Task status updated')
            return redirect('update_task', task_id=task.id)

        if action == 'add_comment':
            content = request.POST.get('content', '').strip()
            if content:
                TaskComment.objects.create(task=task, author=request.user, content=content)
                notify_user(
                    recipient=task.assigned_to,
                    actor=request.user,
                    message=f'New comment on task: {task.title}',
                    task=task,
                )
            return redirect('update_task', task_id=task.id)

    return render(
        request,
        'update_task.html',
        {
            'task': task,
            'comments': task.comments.select_related('author').all(),
            'status_choices': ['Pending', 'In Progress', 'Done'],
        },
    )


@user_passes_test(is_admin)
def delete_task(request, task_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid delete request.')
        return redirect('task_list')

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('task_list')


@user_passes_test(is_admin)
def users_view(request):
    users = User.objects.filter(is_superuser=False).order_by('username')
    return render(request, 'users.html', {'users': users})


@user_passes_test(is_admin)
@require_POST
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account from here.')
        return redirect('users')

    if user.is_superuser:
        messages.error(request, 'Superuser accounts cannot be deleted from this page.')
        return redirect('users')

    try:
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully.')
    except Exception:
        messages.error(request, 'Unable to delete this user right now. Please try again.')
    return redirect('users')


@user_passes_test(is_admin)
@require_POST
def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    new_password = request.POST.get('new_password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()

    if not new_password:
        messages.error(request, 'Password cannot be empty.')
        return redirect('users')

    if new_password != confirm_password:
        messages.error(request, 'Passwords do not match.')
        return redirect('users')

    user.set_password(new_password)
    user.save()
    messages.success(request, f'Password updated for {user.username}.')
    return redirect('users')


@login_required
def notifications_view(request):
    if request.user.is_superuser:
        notifications = Notification.objects.all()   # ✅ ADMIN sees all
    else:
        notifications = Notification.objects.filter(recipient=request.user)

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_notifications_count': notifications.filter(is_read=False).count(),
    })


@login_required
@require_POST
def toggle_notification_read(request, notification_id):
    if request.user.is_superuser:
        notification = get_object_or_404(Notification, id=notification_id)
    else:
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )

    notification.is_read = not notification.is_read
    notification.save(update_fields=['is_read'])

    return redirect('notifications')

@login_required
@require_POST
def mark_all_notifications(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications')