from django.conf import settings


def nolsatu_context(request):

    return {
        'nolsatu_course_home_page': settings.NOLSATU_COURSE_HOST,
    }
