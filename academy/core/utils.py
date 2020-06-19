import datetime
import feedparser
import jwt
import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils import timezone
from django.utils.text import slugify
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


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


def sync_keycloak_user(id_token_object):
    UserModel = get_user_model()

    if getattr(settings, "KEYCLOAK_USE_PREFERRED_USERNAME", False):
        username = id_token_object['preferred_username']
    else:
        username = id_token_object['sub']

    if getattr(settings, "KEYCLOAK_USE_EMAIL_AS_USER_KEY", False):
        user, _ = UserModel.objects.update_or_create(
            email=id_token_object.get('email', ''),
            defaults={
                'username': username,
                'first_name': id_token_object.get('given_name', ''),
                'last_name': id_token_object.get('family_name', '')
            }
        )
    else:
        user, _ = UserModel.objects.update_or_create(
            username=id_token_object.get('email', ''),
            defaults={
                'email': id_token_object.get('email', ''),
                'first_name': id_token_object.get('given_name', ''),
                'last_name': id_token_object.get('family_name', '')
            }
        )

    return user


def call_internal_api(method, url, **kwargs):
    method_map = {
        'get': requests.get,
        'post': requests.post,
        'put': requests.put,
        'patch': requests.patch,
        'delete': requests.delete
    }

    payload = jwt.encode({
        'server_key': settings.SERVER_KEY,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }, settings.SECRET_KEY).decode('utf-8')

    headers = {
        "authorization": f'Server {payload}'
    }

    return method_map[method](url, headers=headers, **kwargs)