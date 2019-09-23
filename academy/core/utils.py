import datetime
import feedparser
from typing import List

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def image_upload_path(prefix='etc', use_dir_date=True):
    if use_dir_date:
        path = f"images/{prefix}/%Y/%m/%d"
    else:
        path = f"images/{prefix}"

    return path


def file_upload_path(prefix='etc'):
    return f"files/{prefix}/%Y/%m/%d"


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


def pagination(data, page, lenght=25):
    paginator = Paginator(data, lenght)
    try:
        data_pagination = paginator.page(page)
    except PageNotAnInteger:
        data_pagination = paginator.page(1)
    except EmptyPage:
        data_pagination = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    index = data_pagination.number
    start_index = max_index - 5 if index > max_index - 3 else (index - 3 if index > 3 else 0)
    end_index = 5 if index <= 3 else (index + 2 if index < max_index - 2 else max_index)
    page_range = list(paginator.page_range)[start_index:end_index]
    return (data_pagination, page_range)


def get_feed_blog(url: str, limit: int = 10) -> dict:
    response = feedparser.parse(url)
    posts = response['entries']
    data = {
        "source": {
            "name": response["feed"]["title"],
            "link": response["feed"]["link"]
        },
        "posts": posts[:limit]
    }
    return data
