from django.conf import settings

from academy.api.gateway.gate import gate

app_name = "gateway"

urlpatterns = list(map(lambda item: gate(item[0], item[1]), settings.API_GATEWAY))
