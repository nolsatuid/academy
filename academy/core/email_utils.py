def construct_email_args(recipients, subject, content, priority=None):
    from academy.apps.offices.models import ConfigEmail

    config = ConfigEmail.objects.get(id=1)
    kwargs = {
        'recipients': recipients,
        'sender': config.from_email,
        'subject': subject,
        'html_message': content
    }

    if priority:
        kwargs['priority'] = priority

    return kwargs
