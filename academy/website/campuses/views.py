from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from academy.website.accounts.forms import SignupForm, ProfileForm, StudentForm
from academy.apps.campuses.models import Campus
from academy.apps.students.models import Training


def index(request):
    campuses = Campus.objects.all()
    context = {
        'title': 'Kampus',
        'campuses': campuses
    }
    return render(request, "website/campuses/index.html", context=context)


def register(request, campus_id):
    campus = get_object_or_404(Campus, id=campus_id)
    if not campus.open_registration:
        messages.warning(request, f"{campus.name} belum membuka pendaftaran")
        return redirect('website:campuses:index')

    if request.user.is_authenticated:
        return redirect('website:accounts:index')

    form = SignupForm(request.POST or None)
    if form.is_valid():
        # set data registration on session to pass profile form
        request.session['registration_data'] = request.POST
        messages.success(request, 'Lanjutkan melengkapi data profil')
        return redirect('website:campuses:complete_profile', campus.id)

    context = {
        'form': form,
        'title': 'Daftar',
        'campus': campus,
        'page': 'campus-registration'
    }
    return render(request, 'website/campuses/form-register.html', context)


def complete_profile(request, campus_id):
    """ This view is used to create users, profiles and students based on the chosen campus
    """
    campus = get_object_or_404(Campus, id=campus_id)
    if not request.session.get('registration_data', None):
        return redirect('website:campuses:index')

    signup_form = SignupForm(request.session['registration_data'])
    form = ProfileForm(
        data=request.POST or None, files=request.FILES or None,
        cv_required=False
    )
    if signup_form.is_valid() and form.is_valid():
        user = signup_form.save()
        form.save(user)

        training = Training.objects.filter(batch__contains="NSC").last()
        if not training:
            training = Training.objects.create(batch="NSC-0")

        form_student = StudentForm(data={'user': user.id, 'training': training.id, 'campus': campus.id})
        if form_student.is_valid():
            form_student.save()
            messages.success(request, 'Mohon cek email Anda untuk mengaktifkan akun')

            # set session to None after complete register
            request.session['registration_data'] = None
            return redirect("website:accounts:login")

    context = {
        'title': 'Lengkapi Profil Anda',
        'form': form,
        'page': 'campus-registration'
    }
    return render(request, 'accounts/index.html', context)