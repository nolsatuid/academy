import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from datetime import datetime, timedelta

from academy.api.serializers import user_profile
from academy.apps.accounts.models import Instructor
from academy.apps.accounts.models import User
from academy.apps.offices.models import LogoPartner, LogoSponsor, Page
from academy.apps.students.models import Student
from academy.apps.graduates.models import Graduate
from academy.core.utils import call_internal_api

from .forms import CertificateVerifyForm
from meta.views import Meta


def index(request):
    meta = Meta(
        description='''NolSatu adalah Talent Hub dari Btech, Para peserta akan mendapatkan materi seputar DevOps, \
Cloud Computing, Python dan pemrograman lainnya. Instruktur pemberi materi juga praktisi dilapangan, ketika memberikan materi \
jadi dapat sharing tentang kondisi dunia TIK  terkini. Tools yang digunakan pun berbasis Open Source, sehingga menambah \
add unique value jika kita mampu menguasai dan mengoptimalkannya. Peserta akan mendapatkan setiap proses itu. \
Dan ingat, setiap menit yang kalian luangkan untuk membaca ini. Ada ratusan bahkan ribuan orang juga yang ingin \
mendaftar. So, segera daftar karena setiap angkatan pun terbatas. NolSatu gratis, karena kami tau. Semua berawal dari Nol, \
lalu menjadi Satu. Di NolSatu.''',
        keywords=[
            'NolSatu', 'Open Source', 'Pelatihan', 'Gratis',
            'Cloud Computing', 'DevOps', 'Btech', 'Pemrograman'
        ],
        image=settings.HOST + '/static/website/images/logo/logo-polos-warna-30.png',
        use_og=True,
        use_facebook=True
    )

    seleksi = Student.objects.pre_test().count()
    peserta = Student.objects.participants().count()
    context = {
        'title': 'Home',
        'mobile_layout': False,
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
    navbar = request.GET.get('navbar')

    context = {
        'title': 'Tilil (Q&A)',
        'navbar': navbar
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
    courses = call_internal_api('get', url=settings.HOST + f'/api/course/list').json()
    
    context = {
        'title': 'Home',
        'courses': courses[:3],
        'course_link': f'{settings.NOLSATU_COURSE_HOST}'
    }
    return render(request, 'website/home-adinusa.html', context)
