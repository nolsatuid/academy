import datetime

from django.utils import timezone


def image_upload_path(prefix='etc'):
    path = f"images/{prefix}/%Y/%m/%d"
    return path


def convert_to_datetime(date, tzinfo=None):
    """
    Converts date objects into timezone aware datetime object
    """
    if isinstance(date, datetime.date):
        date = timezone.make_aware(datetime.datetime.combine(date, datetime.time()),
                                   tzinfo or timezone.get_current_timezone())
    return date


def normalize_datetime_range(start, end, tzinfo=None):
    """
    Function to ensure both start and end are timezone aware
    and ensure start starts at 0:0:0 and end ends at 23:59:59
    """
    start = convert_to_datetime(start, tzinfo)
    end = convert_to_datetime(end, tzinfo)

    start = start.replace(hour=00, minute=00, second=00)
    end = end.replace(hour=23, minute=59, second=59)

    return start, end