from django.http import HttpResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from academy.core.utils import pagination
from academy.apps.campuses.models import Campus
from academy.apps.students.models import Student
from academy.apps.accounts.models import User
from academy.backoffice.campuses.forms import CampusForm, ParticipantsFilterForm, BaseFilterForm


@staff_member_required
def index(request):
    campus_list = Campus.objects.order_by('name')

    context = {
        'title': 'Kampus',
        'menu_active': 'campus',
        'campuses': campus_list
    }
    return render(request, 'backoffice/campuses/index.html', context)


@staff_member_required
def add(request):
    form = CampusForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah kampus')
        return redirect('backoffice:campuses:index')

    context = {
        'title': 'Tambah Kampus',
        'menu_active': 'campus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    campus = get_object_or_404(Campus, id=id)
    form = CampusForm(request.POST or None, request.FILES or None, instance=campus)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit kampus')
        return redirect('backoffice:campuses:index')

    context = {
        'title': 'Edit Kampus',
        'menu_active': 'campus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    campus = get_object_or_404(Campus, id=id)
    campus.delete()
    messages.success(request, 'Berhasil hapus kampus')
    return redirect('backoffice:campuses:index')


@staff_member_required
def details(request, id):
    campus = get_object_or_404(Campus, id=id)

    context = {
        'title': 'Edit Kampus',
        'menu_active': 'campus',
        'campus': campus
    }
    return render(request, 'backoffice/campuses/details.html', context)


class ParticipantsView(View):
    form_class = ParticipantsFilterForm
    template_name = 'backoffice/campuses/participant.html'
    user_ids = Student.objects.filter(status=Student.STATUS.participants, campus__isnull=False) \
        .exclude(user__username='deleted').distinct('user_id').values_list('user_id', flat=True)
    title = 'Peserta'
    page_active = 'participants'
    file_title = 'daftar-peserta-nolsatu-kampus.csv'

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        user_list = User.objects.exclude(is_superuser=True).exclude(is_staff=True) \
            .filter(id__in=self.user_ids)
        user_count = user_list.count()

        download = request.GET.get('download', '')
        form = self.form_class(request.GET or None)
        if form.is_valid():
            user_list = form.get_data()
            if download:
                csv_buffer = form.generate_to_csv()
                response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
                response['Content-Disposition'] = f'attachment; filename={self.file_title}'
                return response

        page = request.GET.get('page', 1)
        users, page_range = pagination(user_list, page)

        context = {
            'title': self.title,
            'menu_active': 'campus',
            'users': users,
            'form': form,
            'user_count': user_count,
            'filter_count': user_list.count(),
            'query_params': 'name=%s&start_date=%s&end_date=%s&status=%s&batch=%s' % (request.GET.get('name', ''),
                request.GET.get('start_date', ''), request.GET.get('end_date', ''), request.GET.get('status', 2), request.GET.get('batch', '')),
            'page_range': page_range
        }
        return render(request, self.template_name, context)


class UserSelectionView(ParticipantsView):
    form_class = BaseFilterForm
    template_name = 'backoffice/campuses/participant.html'
    user_ids = Student.objects.exclude(status=Student.STATUS.graduate).filter(campus__isnull=False) \
        .exclude(user__username='deleted').distinct('user_id').values_list('user_id', flat=True)
    title = 'Pengguna Nolsatu Kampus'
    page_active = 'user'
    file_title = 'daftar-pengguna-nolsatu-kampus.csv'
