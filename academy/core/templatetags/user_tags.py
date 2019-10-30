from django.template import Library

from academy.apps.accounts.models import Inbox

register = Library()

@register.filter(name='unread_inbox_count')
def unread_inbox_count(user):
    inbox = Inbox.objects.filter(user=user, is_read=False)
    if not inbox:
        return ""

    return inbox.count()
