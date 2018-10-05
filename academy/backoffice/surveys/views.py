from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from academy.apps.surveys.model import Survey
from academy.backoffice.surveys.form import SurveyFilterForm


@staff_member_required
def index(request):
    survey_count = Survey.objects.count()
    survey_list = Survey.objects.all()
    download = request.GET.get('download', '')
    form = SurveyFilterForm(request.GET or None)

    if form.is_valid():
        survey_list = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=daftar-peserta.csv'
            return response

    paginator = Paginator(survey_list, 25)
    page = request.GET.get('page', 1)
    try:
        survey = paginator.page(page)
    except PageNotAnInteger:
        survey = paginator.page(1)
    except EmptyPage:
        survey = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    index = survey.number
    start_index = max_index - 5 if index > max_index - 3 else (index - 3 if index > 3 else 0)
    end_index = 5 if index <= 3 else (index + 2 if index < max_index - 2 else max_index)
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'title': 'Survey',
        'page_active': 'surveys',
        'surveys': survey,
        'form': form,
        'survey_count': survey_count,
        'filter_count': survey_list.count(),
        'query_params': 'work_status=%s&channeled=%s&channeled_when=%s' % (
            request.GET.get('work_status', ''), request.GET.get('channeled', ''), request.GET.get('channeled_when', '')
        ),
        'page_range': page_range
    }
    return render(request, 'backoffice/surveys/index.html', context)
