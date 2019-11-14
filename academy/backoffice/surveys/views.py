from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render

from academy.core.utils import pagination
from academy.apps.surveys.model import Survey
from academy.backoffice.surveys.form import SurveyFilterForm


@staff_member_required
def index(request):
    survey_list = Survey.objects.filter(user__students__isnull=False).all()
    survey_count = survey_list.count()
    download = request.GET.get('download', '')
    form = SurveyFilterForm(request.GET or None)

    if form.is_valid():
        survey_list = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=survey.csv'
            return response

    
    page = request.GET.get('page', 1)
    survey, page_range = pagination(survey_list, page)

    context = {
        'title': 'Survey',
        'menu_active': 'surveys',
        'surveys': survey,
        'form': form,
        'survey_count': survey_count,
        'filter_count': survey_list.count(),
        'query_params': 'name=%s&work_status=%s&channeled=%s&channeled_when=%s&status=%s&channeled_location%s' % (
            request.GET.get('name', ''), request.GET.get('work_status', ''), request.GET.get('channeled', ''),
            request.GET.get('channeled_when', ''), request.GET.get('status', ''), request.GET.get('channeled_location', '')
        ),
        'page_range': page_range
    }
    return render(request, 'backoffice/surveys/index.html', context)
