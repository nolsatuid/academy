import datetime
import xhtml2pdf.pisa as pisa

from io import BytesIO
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template


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


def render_to_pdf(path: str, params: dict):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)
