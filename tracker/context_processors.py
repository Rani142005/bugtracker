from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            count = Notification.objects.filter(is_read=False).count()
        else:
            count = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
    else:
        count = 0

    return {
        'unread_notifications_count': count,              # ✅ for navbar
        'global_unread_notifications_count': count        # ✅ for admin dashboard
    }