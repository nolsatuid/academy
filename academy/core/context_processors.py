from django.conf import settings
from academy.apps.offices.models import Setting


def nolsatu_context(request):
    setting = Setting.get_data()
    print(setting)
    return {
        'nolsatu_course_home_page': settings.NOLSATU_COURSE_HOST,
        'site_name': setting.site_name,
        'color_theme': setting.get_color_theme_display(),
        'sidebar_color': setting.get_sidebar_color_display(),
        'footer_title': setting.footer_title,
        'footer_url': setting.footer_url,
        'hide_logo': setting.hide_logo,
        'brand_logo': setting.get_logo(),
        'brand_logo_dark': setting.get_logo_dark(),
        'brand_logo_light': setting.get_logo_light(),
    }
