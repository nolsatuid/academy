import json
import requests
from json.decoder import JSONDecodeError

from requests.exceptions import ConnectionError

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from datetime import datetime, timedelta

from academy.api.serializers import user_profile
from academy.apps.accounts.models import Instructor
from academy.apps.accounts.models import User
from academy.apps.offices.models import LogoPartner, LogoSponsor, Page, FAQ, CategoryPage
from academy.apps.students.models import Student
from academy.apps.graduates.models import Graduate

from .forms import CertificateVerifyForm
from meta.views import Meta
from academy.apps.offices.models import Setting
from django.db.models import Q


def index(request):
    sett = Setting.get_data()
    img_site = Meta(url=sett.get_logo())
    meta = Meta(
        title=sett.site_name,
        description=sett.site_desc,
        keywords=[
            'NolSatu', 'Open Source', 'Pelatihan', 'Gratis',
            'Cloud Computing', 'DevOps', 'Btech', 'Pemrograman'
        ],
        image=img_site.url,
        use_og=True,
        use_facebook=True,
        use_twitter=True
    )

    seleksi = Student.objects.pre_test().count()
    peserta = Student.objects.participants().count()
    context = {
        'title': 'Home',
        'instructors': Instructor.objects.order_by('order'),
        'pengguna': User.objects.actived().count(),
        'seleksi': seleksi + peserta,
        'peserta': peserta,
        'lulus': Student.objects.graduated().count(),
        'tersalurkan': Graduate.objects.filter(is_channeled=True).count(),
        'logo_partners': LogoPartner.objects.filter(is_visible=True).order_by('display_order'),
        'logo_sponsors': LogoSponsor.objects.filter(is_visible=True).order_by('display_order'),
        'meta': meta
    }
    return render(request, 'website/home.html', context)


def faq(request):
    faqs = FAQ.objects.all()

    context = {
        'title': 'Tilil (Q&A)',
        'faqs': faqs
    }

    return render(request, 'website/faq.html', context)


def certificate_verify(request):
    form = CertificateVerifyForm(request.POST or None)
    result = None

    if form.is_valid():
        student = form.verification()
        if student:
            result = student
        else:
            result = ""

    context = {
        'title': 'Verifikasi Sertifikat',
        'form': form,
        'result': result,
    }

    if request.is_ajax():
        html = loader.render_to_string('website/result-verify.html', context)
        return JsonResponse({'html': html})
    return render(request, 'website/cert-verify.html', context)


def home(request):
    context = {
        'title': 'Home 2'
    }
    return render(request, 'website/home2.html', context)


def about(request):
    context = {
        'title': 'About',
        'mobile_layout': True,
    }
    return render(request, 'website/about.html', context)


def talent(request):
    context = {
        'title': 'Talenta & Proffesional',
        'mobile_layout': True,
    }
    return render(request, 'website/talent.html', context)


def company(request):
    context = {
        'title': 'Perusahaan',
        'mobile_layout': True,
    }
    return render(request, 'website/company.html', context)


def statistic(request):
    seleksi = Student.objects.pre_test().count()
    peserta = Student.objects.participants().count()
    context = {
        'title': 'Statistik',
        'mobile_layout': True,
        'pengguna': User.objects.actived().count(),
        'seleksi': seleksi + peserta,
        'peserta': peserta,
        'lulus': Student.objects.graduated().count(),
        'tersalurkan': Graduate.objects.filter(is_channeled=True).count(),
    }
    return render(request, 'website/statistic.html', context)


def error_404(request):
    return render(request, '404.html', {})


def error_500(request):
    return render(request, '500.html', {})


@login_required
def profile(request):
    return HttpResponse(
        json.dumps(user_profile(request.user)),
        content_type="application/json"
    )


def blog_details(request, slug):
    blog = get_object_or_404(Page, slug=slug)

    context = {
        'title': blog.title,
        'blog': blog,
        'meta': blog.as_meta()
    }
    return render(request, 'website/blog-details.html', context)


def blog_index(request):
    blogs = Page.objects.filter(status=Page.STATUS.publish)

    context = {
        'title': 'Blog',
        'blogs': blogs,
    }

    return render(request, 'website/blogs.html', context)


def home_custom(request):
    try:
        courses = requests.get(settings.HOST + '/api/course/list').json()
        courses = courses[:3]
    except (JSONDecodeError, ConnectionError):
        courses = []

    try:
        vendors = requests.get(settings.HOST + '/api/course/vendor/list').json()
    except (JSONDecodeError, ConnectionError):
        vendors = []

    context = {
        'title': 'Home',
        'courses': courses,
        'vendors': vendors
    }
    return render(request, 'website/home-adinusa.html', context)


def page_category(request, type_content, slug):
    if type_content == 'post':
        cat_page = get_object_or_404(CategoryPage, slug=slug)
        blogs = cat_page.group.all()
        context = {
            'title': cat_page.name,
            'blogs': blogs
        }
        return render(request, 'website/page-category.html', context)
    else:
        blog = get_object_or_404(Page, slug=slug)
        context = {
            'title': blog.title,
            'blog': blog
        }
        return render(request, 'website/page-detail.html', context)


def page_category_detail(request, type_content, categoryslug, slug):
    blog = get_object_or_404(Page, group__slug=categoryslug, slug=slug)

    context = {
        'title': blog.title,
        'blog': blog
    }

    return render(request, 'website/page-category-detail.html', context)


def contact(request):
    context = {
        'title': 'Kontak'
    }

    return render(request, 'website/contact.html', context)
